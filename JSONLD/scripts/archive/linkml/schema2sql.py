import json

# Load JSON schema from a file
with open('schema.json', 'r') as f:
    schema = json.load(f)

def json_type_to_sql_type(json_type):
    mapping = {
        'string': 'TEXT',
        'integer': 'INTEGER',
        'number': 'REAL',
        'boolean': 'BOOLEAN',
        'array': 'BLOB',  # Typically arrays are more complex and need special handling
        'object': 'BLOB'  # Objects typically require a more complex schema
    }
    return mapping.get(json_type, 'TEXT')

def generate_sql(schema):
    table_name = schema.get('title', 'Unknown')
    columns = []

    for prop, details in schema['properties'].items():
        sql_type = json_type_to_sql_type(details['type'])
        column_def = f"{prop} {sql_type}"
        if prop in schema.get('required', []):
            column_def += " NOT NULL"
        columns.append(column_def)

    columns_sql = ",\n  ".join(columns)
    sql = f"CREATE TABLE {table_name} (\n  {columns_sql}\n);"
    
    # Handle nested objects (e.g., addresses)
    for prop, details in schema['properties'].items():
        if details['type'] == 'array' and details['items']['type'] == 'object':
            nested_sql = generate_sql(details['items'])
            sql += f"\n\n{nested_sql}"
    
    return sql

# Generate SQL from JSON schema
sql_schema = generate_sql(schema)
print(sql_schema)

