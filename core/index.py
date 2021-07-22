from django.contrib.algoliasearch import AlgoliaIndex

class PlantsIndex(AlgoliaIndex):
    fields = ('id','name', 'actual_price','selling_price','my_image','slug','about','active','_category','_season','stock','fragrance','maintenance_level','placement','is_active')
    should_index = 'is_active'
    settings = {
        'searchableAttributes': ['name','about'],
        'attributesForFaceting':['_tags','_category','_season','fragrance','maintenance_level','placement','active','stock','selling_price']
        }
    search = {
        "filters":"active=1 AND stock=1"
    }
    index_name = 'my_index'
    tags = 'grade_list'

class CategoryIndex(AlgoliaIndex):
    fields = ('id','name','slug')
    settings = {'searchableAttributes': ['name']}
    index_name = 'my_index_category'
