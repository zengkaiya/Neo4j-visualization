
from Database import *
from neomodel import config


class Model:
    def __init__(self):
        pass

    # Disease methods
    def find_disease_by_id(self, disease_id):
        return Disease.nodes.get_or_none(disease_id=disease_id)

    def find_disease_by_name(self, name):
        return Disease.nodes.filter(name=name).all()

    def find_all_diseases(self):
        return Disease.nodes.all()

    # Chemical methods
    def find_chemical_by_id(self, chemical_id):
        return Chemical.nodes.get_or_none(chemical_id=chemical_id)

    def find_chemical_by_name(self, name):
        return Chemical.nodes.filter(name=name).all()

    def find_all_chemicals(self):
        return Chemical.nodes.all()

    # Relationships
    def find_chemicals_associated_with_disease(self, disease_id):
        disease = self.find_disease_by_id(disease_id)
        if disease:
            return disease.associated_with.all()
        return []

    def find_diseases_associated_with_chemical(self, chemical_id):
        chemical = self.find_chemical_by_id(chemical_id)
        if chemical:
            return chemical.associated_with.all()
        return []

    def find_association_between_disease_and_chemical(self, disease_id, chemical_id):
        disease = self.find_disease_by_id(disease_id)
        chemical = self.find_chemical_by_id(chemical_id)
        if disease and chemical:
            return disease.associated_with.filter(chemical=chemical).all()
        return []


if __name__ == '__main__'：

    model = Model()

    # Find all diseases
    diseases = model.find_all_diseases()
    for disease in diseases:
        print(disease.name)

    # Find chemicals associated with a specific disease