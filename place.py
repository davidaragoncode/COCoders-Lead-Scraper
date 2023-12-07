class Place:
    def __init__(self)-> None:
        self.business_status = 'business_status'
        self.geometry = {'location': {'lat': 'lat', 'lng': 'lng'},
                             'viewport': {'northeast': {'lat': 'lat', 'lng': 'lng'},'southwest': {'lat': 'lat','lng': 'lng'}}}
        self.icon = 'icon'
        self.icon_background_color = 'icon_background_color'
        self.icon_mask_base_uri = 'icon_mask_base_uri'
        self.name = 'name'
        self.opening_hours = {'open_now': 'opening_hours'}
        self.place_id = 'place_id'
        self.plus_code = {'compound_code': 'compound_code', 'global_code': 'global_code'}
        self.rating = 0
        self.reference = 'reference'
        self.scope = 'scope'
        self.types = ['types']
        self.user_ratings_total = 0
        self.vicinity = 'vicinity'
