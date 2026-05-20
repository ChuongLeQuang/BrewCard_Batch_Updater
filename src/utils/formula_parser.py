"""
EN: Excel formula evaluator.
VI: Bộ phân dịch và tính toán công thức Excel.
"""

import re
from datetime import datetime, timedelta
from typing import Any, List
from openpyxl.worksheet.worksheet import Worksheet


class ExcelFormulaEvaluator:
    """
    EN: A class to parse and evaluate Excel-like formulas.
    VI: Lớp phân dịch (AST) dùng để tính toán các công thức kiểu Excel.
    """

    def __init__(self, worksheet: Worksheet):
        self.worksheet = worksheet
        self.tokens = []
        self.pos = 0

    def evaluate(self, formula: str) -> Any:
        """EN: Evaluate the given formula string. VI: Tính toán giá trị của chuỗi công thức được cho."""
        formula = str(formula).strip()
        if formula.startswith("="):
            formula = formula[1:]

        # 1. Bộ từ vựng (Lexer/Tokenizer)
        self.tokens = []
        scanner = re.finditer(
            r"(?P<NUMBER>\d+(?:\.\d+)?)|"
            r'(?P<STRING>\'[^\']*\'|"[^"]*")|'
            r"(?P<RANGE>[A-Z]+\d+:[A-Z]+\d+)|"
            r"(?P<CELL>[A-Z]+\d+)|"
            r"(?P<FUNC>[A-Z_]+)(?=\s*\()|"
            r"(?P<COMP><>|<=|>=|<|>|=)|"
            r"(?P<OP>[+\-*/^&])|"
            r"(?P<LPAREN>\()|"
            r"(?P<RPAREN>\))|"
            r"(?P<COMMA>,)|"
            r"(?P<WS>\s+)",
            formula,
            flags=re.IGNORECASE,
        )
        for match in scanner:
            kind = match.lastgroup
            val = match.group()
            if kind == "WS":
                continue
            if kind in ("FUNC", "CELL", "RANGE"):
                val = val.upper()
            self.tokens.append((kind, val))

        self.pos = 0
        if not self.tokens:
            return ""

        # 2. Xây dựng cây cú pháp AST & Tính toán (Lazy Evaluation)
        try:
            root_node = self._parse_expr()
            if self.pos < len(self.tokens):
                raise SyntaxError(f"Unexpected token at end: {self.tokens[self.pos]}")
            return self._eval_node(root_node)
        except ZeroDivisionError:
            return "#DIV/0!"
        except (TypeError, ValueError):
            return "#VALUE!"
        except NameError:
            return "#NAME?"
        except (SyntaxError, IndexError, AttributeError):
            return "#ERROR!"

    def _match(self, *kinds) -> Any:
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] in kinds:
            tok = self.tokens[self.pos]
            self.pos += 1
            return tok
        return None

    def _to_num(self, val: Any) -> float:
        """EN: Safe cast to float (handles Excel Date). VI: Ép kiểu an toàn sang số."""
        if isinstance(val, datetime):
            delta = val - datetime(1899, 12, 30)
            return delta.total_seconds() / 86400.0
        if isinstance(val, bool):
            return 1.0 if val else 0.0
        if val is None or val == "":
            return 0.0
        try:
            return float(val)
        except ValueError:
            raise TypeError(f"Cannot convert '{val}' to number")

    def _flatten_args(self, args: List[Any]) -> List[Any]:
        flat = []
        for arg in args:
            if isinstance(arg, list):
                flat.extend(self._flatten_args(arg))
            else:
                flat.append(arg)
        return flat

    def _eval_node(self, node: Any) -> Any:
        """EN: Evaluate the AST node. VI: Tính toán giá trị từ cây AST."""
        if not isinstance(node, tuple):
            return node

        kind = node[0]
        if kind == "LITERAL":
            return node[1]
        elif kind == "CELL":
            return self._get_cell_value(node[1])
        elif kind == "RANGE":
            return self._get_range_values(node[1])
        elif kind == "UNARY":
            op, operand = node[1], node[2]
            val = self._to_num(self._eval_node(operand))
            return val if op == "+" else -val
        elif kind == "BINOP":
            left_node, op, right_node = node[1], node[2], node[3]
            if op == "&":
                return str(self._eval_node(left_node)) + str(
                    self._eval_node(right_node)
                )

            l_val = self._eval_node(left_node)
            r_val = self._eval_node(right_node)

            if op in ("+", "-", "*", "/", "^"):
                l_num = self._to_num(l_val)
                r_num = self._to_num(r_val)
                if op == "+":
                    return l_num + r_num
                if op == "-":
                    return l_num - r_num
                if op == "*":
                    return l_num * r_num
                if op == "/":
                    if r_num == 0:
                        raise ZeroDivisionError("Division by zero")
                    return l_num / r_num
                if op == "^":
                    return l_num**r_num
            elif op in ("=", "<>", ">", "<", ">=", "<="):
                try:
                    l_cmp = self._to_num(l_val)
                    r_cmp = self._to_num(r_val)
                except TypeError:
                    l_cmp = str(l_val) if l_val is not None else ""
                    r_cmp = str(r_val) if r_val is not None else ""

                if op == "=":
                    return l_cmp == r_cmp
                if op == "<>":
                    return l_cmp != r_cmp
                if op == ">":
                    return l_cmp > r_cmp
                if op == "<":
                    return l_cmp < r_cmp
                if op == ">=":
                    return l_cmp >= r_cmp
                if op == "<=":
                    return l_cmp <= r_cmp

        elif kind == "FUNC":
            func_name, args = node[1], node[2]
            if func_name == "IF":
                if len(args) != 3:
                    raise SyntaxError("IF requires 3 arguments")
                cond = self._eval_node(args[0])
                if cond:
                    return self._eval_node(args[1])
                else:
                    return self._eval_node(args[2])
            elif func_name == "AND":
                return all(self._to_num(self._eval_node(a)) for a in args)
            elif func_name == "OR":
                return any(self._to_num(self._eval_node(a)) for a in args)
            elif func_name == "NOT":
                return not self._to_num(self._eval_node(args[0]))

            eval_args = [self._eval_node(a) for a in args]
            return self._evaluate_function(func_name, eval_args)

    # --- Đệ quy Phân dịch (Recursive Descent Parser) ---

    def _parse_expr(self) -> Any:
        return self._parse_comp()

    def _parse_comp(self) -> Any:
        left = self._parse_concat()
        while True:
            op = self._match("COMP")
            if not op:
                break
            right = self._parse_concat()
            left = ("BINOP", left, op[1], right)
        return left

    def _parse_concat(self) -> Any:
        left = self._parse_add()
        while True:
            op = self._match("OP")
            if op and op[1] == "&":
                right = self._parse_add()
                left = ("BINOP", left, "&", right)
            else:
                if op:
                    self.pos -= 1
                break
        return left

    def _parse_add(self) -> Any:
        left = self._parse_mul()
        while True:
            op = self._match("OP")
            if op and op[1] in ("+", "-"):
                right = self._parse_mul()
                left = ("BINOP", left, op[1], right)
            else:
                if op:
                    self.pos -= 1
                break
        return left

    def _parse_mul(self) -> Any:
        left = self._parse_exp()
        while True:
            op = self._match("OP")
            if op and op[1] in ("*", "/"):
                right = self._parse_exp()
                left = ("BINOP", left, op[1], right)
            else:
                if op:
                    self.pos -= 1
                break
        return left

    def _parse_exp(self) -> Any:
        left = self._parse_unary()
        while True:
            op = self._match("OP")
            if op and op[1] == "^":
                right = self._parse_unary()
                left = ("BINOP", left, "^", right)
            else:
                if op:
                    self.pos -= 1
                break
        return left

    def _parse_unary(self) -> Any:
        op = self._match("OP")
        if op and op[1] in ("+", "-"):
            val = self._parse_unary()
            return ("UNARY", op[1], val)
        if op:
            self.pos -= 1
        return self._parse_primary()

    def _parse_primary(self) -> Any:
        tok = self._match("NUMBER", "STRING", "CELL", "RANGE", "FUNC", "LPAREN")
        if not tok:
            raise SyntaxError("Unexpected end or invalid token")
        kind, val = tok

        if kind == "NUMBER":
            return ("LITERAL", float(val) if "." in val else int(val))
        if kind == "STRING":
            return ("LITERAL", val[1:-1])
        if kind == "CELL":
            return ("CELL", val)
        if kind == "RANGE":
            return ("RANGE", val)
        if kind == "LPAREN":
            res = self._parse_expr()
            if not self._match("RPAREN"):
                raise SyntaxError("Missing ')'")
            return res
        if kind == "FUNC":
            self._match("LPAREN")
            args = []
            if not self._match("RPAREN"):
                args.append(self._parse_expr())
                while self._match("COMMA"):
                    args.append(self._parse_expr())
                if not self._match("RPAREN"):
                    raise SyntaxError(f"Missing ')' for {val}")
            return ("FUNC", val, args)

    # --- Logic 30+ Hàm Excel (Excel Functions) ---

    def _evaluate_function(self, func_name: str, args: List[Any]) -> Any:
        flat_args = self._flatten_args(args)

        if func_name == "IF":
            raise NameError("IF should be evaluated lazily in _eval_node")
        elif func_name in ("AND", "OR", "NOT"):
            raise NameError(f"{func_name} should be evaluated lazily in _eval_node")

        if func_name == "CONCATENATE":
            return "".join(str(a) for a in flat_args)
        elif func_name == "LEFT":
            return str(args[0])[: int(self._to_num(args[1]) if len(args) > 1 else 1)]
        elif func_name == "RIGHT":
            n = int(self._to_num(args[1]) if len(args) > 1 else 1)
            return str(args[0])[-n:] if n > 0 else ""
        elif func_name == "MID":
            return str(args[0])[
                int(self._to_num(args[1]))
                - 1 : int(self._to_num(args[1]))
                - 1
                + int(self._to_num(args[2]))
            ]
        elif func_name == "LEN":
            return len(str(args[0]))
        elif func_name == "TRIM":
            return str(args[0]).strip()
        elif func_name == "UPPER":
            return str(args[0]).upper()
        elif func_name == "LOWER":
            return str(args[0]).lower()

        if func_name in ("HOUR", "MINUTE", "SECOND"):
            val = args[0]
            dt = (
                val
                if isinstance(val, datetime)
                else datetime(1899, 12, 30) + timedelta(days=self._to_num(val))
            )
            if func_name == "HOUR":
                return dt.hour
            elif func_name == "MINUTE":
                return dt.minute
            return dt.second

        if func_name == "COUNT":
            count = 0
            for arg in flat_args:
                if isinstance(arg, (int, float)):
                    count += 1
            return count

        num_args = [self._to_num(a) for a in flat_args]
        if func_name == "SUM":
            return sum(num_args)
        elif func_name == "AVERAGE":
            return sum(num_args) / len(num_args) if num_args else 0
        elif func_name == "MIN":
            return min(num_args) if num_args else 0
        elif func_name == "MAX":
            return max(num_args) if num_args else 0
        elif func_name == "ABS":
            return abs(num_args[0])
        elif func_name == "ROUND":
            return round(num_args[0], int(num_args[1]) if len(num_args) > 1 else 0)
        elif func_name == "INT":
            return int(num_args[0])
        elif func_name == "MOD":
            return num_args[0] % num_args[1]

        raise NameError(f"Function {func_name} is not supported")

    # --- Tương tác với Openpyxl (Helpers) ---

    def _get_cell_value(self, coord: str) -> Any:
        match = re.match(r"([A-Z]+)(\d+)", coord)
        if not match:
            return 0
        col_str, row_str = match.groups()
        col = 0
        for c in col_str:
            col = col * 26 + (ord(c) - ord("A") + 1)
        try:
            val = self.worksheet.cell(int(row_str), col).value
            return val if val is not None else ""
        except (ValueError, IndexError, AttributeError):
            return ""

    def _get_range_values(self, range_str: str) -> List[Any]:
        start, end = range_str.split(":")
        match1, match2 = re.match(r"([A-Z]+)(\d+)", start), re.match(
            r"([A-Z]+)(\d+)", end
        )
        if not match1 or not match2:
            return []

        c1_str, r1_str = match1.groups()
        c2_str, r2_str = match2.groups()
        c1, c2 = 0, 0
        for c in c1_str:
            c1 = c1 * 26 + (ord(c) - ord("A") + 1)
        for c in c2_str:
            c2 = c2 * 26 + (ord(c) - ord("A") + 1)

        vals = []
        for r in range(
            min(int(r1_str), int(r2_str)), max(int(r1_str), int(r2_str)) + 1
        ):
            for c in range(min(c1, c2), max(c1, c2) + 1):
                try:
                    val = self.worksheet.cell(r, c).value
                    vals.append(val if val is not None else "")
                except (ValueError, IndexError, AttributeError):
                    vals.append("")
        return vals
