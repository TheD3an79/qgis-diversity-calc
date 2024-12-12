import math


def dc_summarisePoly(poly, lyrPoint, fldSpecies):
    ######################################################################
    #
    #   This function takes as inputs the following parameters:
    #       poly        = a single polygon QgsFeature
    #       lyrPoint    = a QgsVectorLayer containing points. Each
    #                     point represents a single observation of a
    #                     species.
    #       fldSpecies  = a string containing the name of the field
    #                     in the points layer that contains the name
    #                     of the species
    #
    #       The purpose of the function is to summarise the number of
    #       observations of each species inside the polygon in the form
    #       of a dictionary containing species as keys and the number of
    #       observations as values

    dctPoly = {}

    # loop through all the points that intersect the polygons bounding box
    for obs in lyrPoint.getFeatures(poly.geometry().boundingBox()):
        # check to see if the point is actually inside the polygon
        if  poly.geometry().contains(obs.geometry()):
            # get the name of the species as a string variable
            sSpecies = obs.attribute(fldSpecies)
            # check to see if the species already has an entry in the dictionary
            if sSpecies in dctPoly.keys():
                # increase the count by 1
                dctPoly[sSpecies] += 1
            else:
                # if there is no entry for the species, create it and set its
                # initial value to 1
                dctPoly[sSpecies] = 1

    return dctPoly

def dc_mergeDictionaries(dMain, cat, dPoly):
    #######################################################################################
    #
    #   This function takes as inputs the foloowing paameters:
    #       dMain   = a dictionary with categories as the key and another
    #                 dictionary containing the summary information as the value
    #       cat     = a string containing the name of the category to be merged
    #       dPoly   = a dictionary containing summary information for a polygon
    #                (created by the dc_summarisePoly function). The keys are the
    #                names of the species occuring in the polygon and the values
    #                are the number of of observations of that species in the polygon
    #
    #   The purpose of the function is to merge the species counts from dPoly into
    #   the appropriate summary information in dctMain

    # check to see if the category exists in the main dictionary
    if cat in dMain.keys():
        # if it does then loop through the smmary data in dPoly
        for species, obs in dPoly.items():
            # check to see if there is already an entry for the species in this category
            if species in dMain[cat].keys():
                # if there s then add the number of observations in the summary data
                dMain[cat][species] += obs
            else:
                # if there isn't then create a new entry for the species and set the
                # number of observations as the initial value
                dMain[cat][species] = obs
    else:
        # if it doesn't then create an entry for the category with the summary
        # dictionary as the initial value
        dMain[cat] = dPoly

    return dMain


def dc_richness(dict):
    #######################################################################
    #   This function takes as inputs the following parameters:
    #       Dict = a dictionary containing summary information for a polygon
    #              The keys are the names of the species occuring in the polygon
    #              And the values are the number of observations of that species
    #              In the polygon
    #
    #   The purpose of the function is to calculate species richness from the dict
    #   Provided above, which is just the total number of species observed or the
    #   Length of the dictionaries

    return len(dict)


def dc_shannons(dict):
    #######################################################################
    #   This function takes as inputs the following parameters:
    #       Dict = a dictionary containing summary information for a polygon
    #              The keys are the names of the species occuring in the polygon
    #              And the values are the number of observations of that species
    #              In the polygon
    #
    #   The purpose of the function is to calculate Shannons diversity index
    #   from the dict provided above

    # first calculate the total number of observations
    total = sum(dict.values())

    # set the initial value to 0
    shannons = 0

    # loop through all the species counts in the dictionary
    for count in dict.values():
        # calculate the proportion of total observations
        prop = count/total

        shannons += prop*math.log(prop)

    return abs(shannons)


def dc_simpsons(dict):
    #######################################################################
    #   This function takes as inputs the following parameters:
    #       Dict = a dictionary containing summary information for a polygon
    #              The keys are the names of the species occuring in the polygon
    #              And the values are the number of observations of that species
    #              In the polygon
    #
    #   The purpose of the function is to calculate Simpsons diversity index
    #   from the dict provided above

    # first calculate the total number of observations
    total = sum(dict.values())

    # set the initial value to 0
    simpsons = 0

    # loop through all the species counts in the dictionary
    for count in dict.values():
        # calculate the proportion of total observations
        prop = count / total

        simpsons += prop * prop

    return simpsons


def dc_evenness(dict):
    #######################################################################
    #   This function takes as inputs the following parameters:
    #       Dict = a dictionary containing summary information for a polygon
    #              The keys are the names of the species occuring in the polygon
    #              And the values are the number of observations of that species
    #              In the polygon
    #
    #   The purpose of the function is to calculate species evenness index from
    #   the dict provided above. Evenness will be 1 when all the species have the
    #   same number of observations and lower values as some species have greate
    #   numbers of observations than others

    # maximum value that Shannons index can be is the log of the total number of species (richness)
    max = math.log(dc_richness(dict))
    return dc_shannons(dict)/max


def dc_resultString(dict):
    result = ""
    for categoy, summary in dict.items():
        result += "{}: {}  {:2.3f}  {:2.3f}  {:2.3f}\n".format(categoy,
                                                             dc_richness(summary),
                                                             dc_shannons(summary),
                                                             dc_simpsons(summary),
                                                             dc_evenness(summary))

    return result














