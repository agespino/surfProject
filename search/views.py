from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader, Context
from .forms import SearchCompoundForm 
from .pubChemRetrieve import getCompound, getResults
from .parseInchi import getConnectivityMatrix, atomsList, getLabeledM, findBondWeightsM, getRings, getSymmClasses
from .calcBeta import getPrimSecTert, getBetas
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D

# Create your views here.
def index(request):
    template = loader.get_template('search/index.html')
    context, query =  getQuery(request)
    
    

    if(request.method == 'POST'):
        print('redirect')
        # return redirect('search:search-results')
        queryType = 'name'
        c = getCompound(query, queryType)

        return HttpResponseRedirect(reverse('search:search-results-list', args = (queryType, query, )))

        #if c != None:
        #    return HttpResponseRedirect(reverse('search:search-results', args = (queryType, query, )))

    return HttpResponse(template.render(context, request))

def getQuery(request): 
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchCompoundForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            query = form.clean_query()
            return ({'form': form}, query)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchCompoundForm()

    return  ({'form': form}, None)

def getQueryType(request):
    pass

def resultsLstView(request, queryType, query):
    template = loader.get_template('search/resultsList.html')

    results = getResults(query, queryType)
    print("num results", len(results))

    context = {"resultsLst": results}

    return HttpResponse(template.render(context, request))

def results(request, queryType, query):
    template = loader.get_template('search/result.html')

    name, inchi, smiles =  getCompound(query, queryType)

    cTable = getConnectivityMatrix(inchi)
    atoms = atomsList(inchi)

    boTable = findBondWeightsM(cTable, atoms, inchi)
    


    m = Chem.inchi.MolFromInchi(inchi)
    symmGroups = getSymmClasses(Chem.AddHs(m))
    sssr = getRings(m)
    hasRings = False 

    if len(sssr) > 0:
        hasRings = True 

    drawer = rdMolDraw2D.MolDraw2DSVG(400,200)

    prim, sec, tert = getPrimSecTert( boTable, [] , 0 )
    

    print("prim: ", prim)
    print("sec: ",sec)
    print("ter: ",tert)
    

    context = {'name': name, 'inchiStr': inchi,
        'smilesStr': smiles, 
        'cTableSimple': getLabeledM(cTable, atoms, True, False),
        'boTableSimple': getLabeledM(boTable, atoms, True, False),
        'cTableFull': getLabeledM(cTable, atoms, True, True),
        'boTableFull': getLabeledM(boTable, atoms, True, True),
        'hasRings': hasRings,
        'betas': getBetas(boTable, [], atoms),
        'ringsLst': sssr,
        'molSvg': Chem.Draw.MolToImage(m, size = (600, 600)),
        'symmGroups': symmGroups
        }

    return HttpResponse(template.render(context, request))
    