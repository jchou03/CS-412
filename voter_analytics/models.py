from django.db import models

# Create your models here.
class Voter(models.Model):
    '''class modeling a voter'''
    
    # name fields
    first_name = models.TextField()
    last_name = models.TextField()
    
    # address fields
    address_street_number = models.IntegerField()
    address_street_name = models.TextField()
    address_apt_number = models.TextField()
    address_zip_code = models.IntegerField()
    
    # misc information fields
    birth_date = models.DateField()
    register_date = models.DateField()
    party = models.CharField(max_length=1)
    precinct = models.IntegerField()
    
    # previous voting fields
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    
    voter_score = models.IntegerField()
    
    def __str__(self):
        '''string representation of the voter'''
        return f'{self.first_name} {self.last_name}'
    
def bool_value(string: str):
    if string.upper() == "TRUE":
        return True
    elif string.upper() == "FALSE":
        return False
    else:
        return None
    
def load_data():
    '''function to load the data from the csv file'''
    filename = '/Users/jared/Downloads/newton_voters.csv'
    f = open(filename)
    # remove the header lines
    f.readline() 
    for line in f:
        fields = line.split(',')
        # print(fields)
        try:
            voter = Voter(first_name=fields[2],
                      last_name=fields[1],
                      address_street_number=fields[3],
                      address_street_name=fields[4],
                      address_apt_number=fields[5],
                      address_zip_code=fields[6],
                      birth_date=fields[7],
                      register_date=fields[8],
                      party=fields[9],
                      precinct=fields[10],
                      v20state=bool_value(fields[11]),
                      v21town=bool_value(fields[12]),
                      v21primary=bool_value(fields[13]),
                      v22general=bool_value(fields[14]),
                      v23town=bool_value(fields[15]),
                      voter_score=int(fields[16][0]))
            voter.save()
            print(f'created voter {voter}')

        except Exception as e:
            print(f'exception occurred {e}')
            print(f'fields: {fields}')
            break
            
    print(f'done importing all data')