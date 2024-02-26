from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=280)

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    TYPES = (
            ("SEDAN", "Sedan"), ("SUV", "SUV"), ("WAGON", "Wagon"), ("LIMOUSINE", "Limousine"), ("PICKUP", "Pickup")
        )

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    c_type = models.CharField(max_length=30, choices=TYPES)
    dealer_id = models.IntegerField()
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + \
                " Make Name: "+ self.make.name + \
                " Type: " + self.c_type + \
                " Dealer ID: " + str(self.dealer_id)+ \
                " Year: " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # Optional attributes
        self.purchase_date = ""
        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)
