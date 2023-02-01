"""this file contains the database model that will be used to enter data into
the database. it will use an ORM to ensure the data is inform of an object"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///vulnerabilities.db", future=True)

Base = declarative_base()


class Vulnerability(Base):
    __tablename__ = "vulnerability"
    id = Column(String(30), primary_key=True)
    description = Column(String(1000))

    countermeasures = relationship(
                    "Countermeasure",
                    back_populates="vulnerability",
                    cascade="all,delete-orphan"
    )

    def __repr__(self):
        return f'{self.id}'


class VulnTree(Base):
    __tablename__ = "vuln_tree"
    id = Column(Integer, primary_key=True)
    root_node = Column(String(30))
    # complexity = Column(Integer, default=0)
    children = relationship("Children", back_populates="vuln_tree")

    def __repr__(self):
        return f'Tree: {self.id}, {self.base_node}'


class Children(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True)
    my_id = Column(String(30))
    tree_id = Column(String(30), ForeignKey("vuln_tree.id"), nullable=False)
    parent_id = Column(String(30))
    edu_complexity = Column(Integer)
    vuln_tree = relationship("VulnTree", back_populates='children')

    def __repr__(self):
        return f'{self.my_id} child of {self.parent_id} in {self.tree_id}'


class Countermeasure(Base):
    __tablename__ = 'countermeasures'
    id = Column(Integer, primary_key=True)
    text = Column(String(1000))
    vuln_id = Column(String(30), ForeignKey("vulnerability.id"), nullable=False)
    vulnerability = relationship("Vulnerability", back_populates="countermeasures")
