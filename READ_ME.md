# How to run this program

 For now, the program can only accept search name for vulnerabilities from the database. 
 Running <code>main.py</code> will prompt you for the CVE number.
 
## Modules
The module <code> helpers.py</code> contains the code that i used to load the CVE data into
the database.

<code>model.py</code> contains the database model<br>
<code>vulnerabilityNode</code> and <code>vulnerability_tree.py</code> contain classes
that describe the interfaces for the objects that will be nodes in the vulnerability tree.

run <code>pip install -r requirements.txt</code> to download the necessary packages
for the virtual environment.