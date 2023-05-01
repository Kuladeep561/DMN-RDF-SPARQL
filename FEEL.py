import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class UnsupportedArithmeticOperation(Exception):
    pass

class DataUpdater:
    
    @staticmethod
    def is_feel_expression(expression: str) -> bool:
        return "date and time(" in expression

    @staticmethod
    def extract_referenced_column(feel_expression: str) -> str:
        return re.search(r'\((.*?)\)', feel_expression).group(1)

    def update_output_data(self, input_data: Dict[str, List[str]], output_data: Dict[str, List[str]]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        updated_output_data = {key: [] for key in output_data.keys()}

        max_length = max(len(value_list) for value_list in output_data.values())

        for i in range(max_length):
            for key, value_list in output_data.items():
                if i < len(value_list):
                    value = value_list[i]

                    if self.is_feel_expression(value):
                        column_name = self.extract_referenced_column(value)
                        duration_str = re.search(r'duration\("(.*?)"\)', value).group(1)
                        operation_match = re.search(r'([+-])', value)

                        if operation_match is None:
                            raise UnsupportedArithmeticOperation(f"Unsupported arithmetic operation in the expression: {value}")

                        operation = operation_match.group(1)

                        activity_start_date_str = input_data[column_name][i][15:-2]

                        activity_start_date = datetime.fromisoformat(activity_start_date_str.replace("Z", "+00:00"))

                        duration_days = int(duration_str[1:-1])
                        if operation == "+":
                            new_date = activity_start_date + timedelta(days=duration_days)
                        elif operation == "-":
                            new_date = activity_start_date - timedelta(days=duration_days)
                        else:
                            raise UnsupportedArithmeticOperation(f"Unsupported arithmetic operation: {operation}")

                        new_date_str = new_date.replace(tzinfo=None).isoformat() + "Z"
                        updated_output_data[key].append(new_date_str)

                    else:
                        updated_output_data[key].append(value)

            # Update the input_data dictionary by removing the 'date and time()' wrapper from the date string
            #input_data[column_name][i] = activity_start_date_str

        return input_data, updated_output_data
