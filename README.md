# TSpec Module

A simple Python module that allows the user to create <a href="https://saas.hpe.com/en-us/software/quality-center">Quality Center</a>-compatible test specifications.

## Installation

Use the option --record to keep track of the files created during the installation:
```bash
git clone https://github.com/JGalego/TSpec.git
cd TSpec
python setup.py install --record files.txt
python -c "import tspec"
```

Use the following command to uninstall:
```bash
cat files.txt | xargs rm -rf
```

## Example

```python
#!/usr/bin/env python
# -*- coding: utf8 -*-

"""TSpec Example"""

###########
# Modules #
###########

from itertools import product
from tspec import TestStep
from tspec import BasicTest
from tspec import TestSpec

###########
# M A I N #
###########

# Test Variables
SUBJECTS = ("John", "Paul", "Ringo", "George")
CALCULATOR_BRAND_PRICES = (("Casio", "100€"), \
                           ("Texas Instruments", "200€"))

# Initialize TSpec
TSPEC = TestSpec("FeatureX")

# Main Loop
for (subject, (calculator, price)) in product(SUBJECTS, CALCULATOR_BRAND_PRICES):
    test = BasicTest("%s_%s" % (subject, calculator))
    test.translate_name() #QC-compatible test-name

    # Description (Design Steps)
    design_steps = [("%s goes into the store" % subject, \
                     "%s is inside the store" % subject), \
                    ("%s buys a %s calculator" % (subject, calculator), \
                     "The calculator costs %s" % price)]


    for ds in design_steps:
        test.append_test_step(TestStep(design_steps.index(ds)+1, ds[0], ds[1]))

    TSPEC.add_test(test)

# Generate TSpec CSV
TSPEC.convert_to_csv()
```

## Output

| test_id | step_id | description | expected_result |
|---|---|---|---|
| John_Casio | 1 | John goes into the store | John is inside the store |
|  | 2 | John buys a Casio calculator | The calculator costs 100€ |
| John_Texas_Instruments | 1 | John goes into the store | John is inside the store |
|  | 2 | John buys a Texas Instruments calculator | The calculator costs 200€ |
| Paul_Casio | 1 | Paul goes into the store | Paul is inside the store |
|  | 2 | Paul buys a Casio calculator | The calculator costs 100€ |
| Paul_Texas_Instruments | 1 | Paul goes into the store | Paul is inside the store |
|  | 2 | Paul buys a Texas Instruments calculator | The calculator costs 200€ |
| Ringo_Casio | 1 | Ringo goes into the store | Ringo is inside the store |
|  | 2 | Ringo buys a Casio calculator | The calculator costs 100€ |
| Ringo_Texas_Instruments | 1 | Ringo goes into the store | Ringo is inside the store |
|  | 2 | Ringo buys a Texas Instruments calculator | The calculator costs 200€ |
| George_Casio | 1 | George goes into the store | George is inside the store |
|  | 2 | George buys a Casio calculator | The calculator costs 100€ |
| George_Texas_Instruments | 1 | George goes into the store | George is inside the store |
|  | 2 | George buys a Texas Instruments calculator | The calculator costs 200€ |
