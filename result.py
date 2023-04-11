
from tabulate import tabulate

class Result:
    pass

class TextResult(Result):
    def __init__(self, text):
        self.text = text
    def show(self):
        print("A:", self.text)
    def object(self):
        return {
            "class": "text",
            "answer": self.text,
        }

class TableResult(Result):
    def __init__(self, table, cells):
        self.table = table
        self.cells = cells
    def show(self):
        rows = [ row[0] for row in self.cells]
        table = self.table.iloc[rows, :]
        print()
        print(tabulate(
            table, showindex=False, headers="keys", tablefmt="pretty"
        ))
    def object(self):

        rows = [ row[0] for row in self.cells]
        table = self.table.iloc[rows, :]

        return {
            "class": "table",
            "columns": table.columns.to_list(),
            "table": table.to_dict(orient='list'),
        }
