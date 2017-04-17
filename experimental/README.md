## Example

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
