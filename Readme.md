A IPython kernel for Idris
============================

Unsophisticated Idris IPython kernel. Don't expect robustness.

# Installation

Download the contents of the repository and run:

```bash
python install.py
```

# Use

Any of the following:

```bash
jupyter console --kernel i2dris
jupyter qtconsole --kernel i2dris
# Or run the following and  "New File -> Idris"
jupyter notebook
```

# Known issues

``where`` statements seems to be ignored by the ":let" command which the kernel uses to evaluate statements. In the future, I hope this can be rectified by making using of a home-made version of Idris's IDE mode.



