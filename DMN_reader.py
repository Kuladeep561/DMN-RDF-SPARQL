import xml.etree.ElementTree as ET
import re
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class UnsupportedArithmeticOperation(Exception):
    pass

class DMNParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = ET.parse(self.filepath)
        self.root = self.tree.getroot()
        self.xml_namespace = {'xmldmn': 'https://www.omg.org/spec/DMN/20191111/MODEL/'}

    def extract_hit_policy(self):
        decision_table = self.root.find('.//xmldmn:decisionTable', self.xml_namespace)
        hit_policy = decision_table.get('hitPolicy')
        return hit_policy
    
    def extract_variables(self):

        # Extract input and output variables
        self.input_variables = [txt.text for i in self.root.findall('.//xmldmn:inputExpression', self.xml_namespace) for txt in i.findall('.//xmldmn:text', self.xml_namespace)]
        self.output_variables = [i.get('name') for i in self.root.findall('.//xmldmn:output', self.xml_namespace)]
        
        return self.input_variables, self.output_variables

    def extract_inputs_outputs(self):

        self.extract_variables()
        
        # Initialize inputs and outputs
        self.inputs = {var: [] for var in self.input_variables}
        self.outputs = {var: [] for var in self.output_variables}


        all_rules = self.root.findall('.//xmldmn:rule', self.xml_namespace)
        all_rules.pop()

        # Loop through all rules
        for rule in all_rules:
            # Extract input entries
            allinput_entries = rule.findall('.//xmldmn:inputEntry//xmldmn:text', self.xml_namespace)
            for i, txt in enumerate(allinput_entries):
                self.inputs[self.input_variables[i]].append(txt.text)

            # Extract output entries
            alloutput_entries = rule.findall('.//xmldmn:outputEntry//xmldmn:text', self.xml_namespace)
            for i, txt in enumerate(alloutput_entries):
                self.outputs[self.output_variables[i]].append(txt.text)

        return self.inputs, self.outputs
    
    def strip_quotes(self, input_val=None, output_val=None):
        self.extract_inputs_outputs()

        if input_val is None:
            input_val = self.inputs
        if output_val is None:
            output_val = self.outputs
        for key in input_val:
            for i, val in enumerate(input_val[key]):
                input_val[key][i] = val.strip('/"')

        for key in output_val:
            for i, val in enumerate(output_val[key]):
                output_val[key][i] = val.strip('/"')
        return input_val, output_val

    def is_feel_expression(self,expression: str) -> bool:
        return "date and time(" in expression
    def extract_referenced_column(self, feel_expression: str) -> str:
        return re.search(r'\((.*?)\)', feel_expression).group(1)
    
    def FEEL_converter(self, input_data: Dict[str, List[str]] = None, output_data: Dict[str, List[str]] = None) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        
        if input_data is None and output_data is None:      
            input_data, output_data = self.strip_quotes(self.inputs, self.outputs)
        else:
              input_data, output_data = self.strip_quotes(input_data, output_data)

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
            input_data[column_name][i] = activity_start_date_str

        return input_data, updated_output_data

    
    
    def extract_text_between_parentheses(self, input_val=None, output_val=None):

        self.strip_quotes()

        if input_val is None:
            input_val = self.inputs
        if output_val is None:
            output_val = self.outputs
        regex = r"\((.*?)\)"
        for key in input_val:
            for i, val in enumerate(input_val[key]):
                match = re.search(regex, val)
                if match:
                    input_val[key][i] = match.group(1)

        for key in output_val:
            for i, val in enumerate(output_val[key]):
                match = re.search(regex, val)
                if match:
                    output_val[key][i] = match.group(1)

        return input_val, output_val

    def dmn_as_dataframe(self, input_val=None, output_val=None):

        self.extract_text_between_parentheses()

        if input_val is None:
            input_val = self.final_inputs
        if output_val is None:
            output_val = self.final_outputs
        df_inputs = pd.DataFrame.from_dict(input_val)
        df_outputs = pd.DataFrame.from_dict(output_val)

        return df_inputs, df_outputs
