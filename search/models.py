from django.db import models

# Create your models here.
class ChemSpecies(models.Model):
	name = models.CharField(max_length = 100)
	inchiCoreLayers = models.CharField(max_length = 200)


class Isotope(models.Model):
	isotopeLayer = models.CharField(max_length = 200)
	inchiCoreLayers = models.ForeignKey('ChemSpecies', max_length = 200, on_delete = models.CASCADE )
	beta_fact = models.FloatField()

class Smiles(models.Model):
	smiles = models.CharField(max_length = 200)
	inchiCoreLayers = models.ForeignKey('ChemSpecies', max_length = 200, on_delete = models.CASCADE )



class BetaFactorsBond():
	bondName = models.CharField(max_length = 100)
	primary = models.FloatField()
	secondary = models.FloatField()
	tertiary = models.FloatField()