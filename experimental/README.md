## Example (QC Connector)

<b>Information:</b> Tested with Python 2.7 (32bit)

```python
from qc_connector import QCConnector

# Initialize QC Connector
qc = QCConnector('http://qc.dummy.com:8090/qcbin')

# Login and Connect
qc.login_and_connect('<username>', '<password>', '<domain>', '<project>')

# Export Tests
qc.export_tests('Subject\\<Node>')

# Disconnect and Logout
qc.disconnect_and_logout()
```

## Example (TSpec Config Parser)

```python
from tspec_config_parser import TestSpecConfigParser

# Initialize TestSpecConfigParser
p = TestSpecConfigParser('sample.tspec')

# Generate TestSpec Object
ts = p.generate_tspec()
print ts

# Convert TestSpec to CSV file
ts.convert_to_csv('example.csv')
```
