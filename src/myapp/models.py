from django.db import models
from django.contrib.auth.models import User
from pinax.eventlog.models import log
from datetime import datetime, timezone
from django.contrib.postgres.fields import ArrayField

class Event(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=300)
    link = models.URLField(blank=True)
    image = models.FileField(upload_to='images/%Y%m%d')
    datetime = models.DateTimeField()
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class Post(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, null=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

class Resource(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=300, blank=True)
    excerpt = models.TextField(blank=True)
    link = models.CharField(max_length=300, blank=True)
    file = models.FileField(upload_to='files/%Y%m%d', blank=True)
    featured = models.BooleanField(default=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.title)

class Job(models.Model):
    user = models.ForeignKey(User)
    company = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    excerpt = models.TextField()
    link = models.CharField(max_length=300)
    image = models.FileField(upload_to='images/%Y%m%d')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Profile(models.Model):
    LOCATION = (
        ('Aberdeen', 'Aberdeen'),
        ('Abilene', 'Abilene'),
        ('Akron', 'Akron'),
        ('Albany', 'Albany'),
        ('Albuquerque', 'Albuquerque'),
        ('Alexandria', 'Alexandria'),
        ('Allentown', 'Allentown'),
        ('Amarillo', 'Amarillo'),
        ('Anaheim', 'Anaheim'),
        ('Anchorage', 'Anchorage'),
        ('Ann Arbor', 'Ann Arbor'),
        ('Antioch', 'Antioch'),
        ('Apple Valley', 'Apple Valley'),
        ('Appleton', 'Appleton'),
        ('Arlington', 'Arlington'),
        ('Arvada', 'Arvada'),
        ('Asheville', 'Asheville'),
        ('Athens', 'Athens'),
        ('Atlanta', 'Atlanta'),
        ('Atlantic City', 'Atlantic City'),
        ('Augusta', 'Augusta'),
        ('Aurora', 'Aurora'),
        ('Austin', 'Austin'),
        ('Bakersfield', 'Bakersfield'),
        ('Baltimore', 'Baltimore'),
        ('Barnstable', 'Barnstable'),
        ('Baton Rouge', 'Baton Rouge'),
        ('Beaumont', 'Beaumont'),
        ('Bel Air', 'Bel Air'),
        ('Bellevue', 'Bellevue'),
        ('Berkeley', 'Berkeley'),
        ('Bethlehem', 'Bethlehem'),
        ('Billings', 'Billings'),
        ('Birmingham', 'Birmingham'),
        ('Bloomington', 'Bloomington'),
        ('Boise', 'Boise'),
        ('Boise City', 'Boise City'),
        ('Bonita Springs', 'Bonita Springs'),
        ('Boston', 'Boston'),
        ('Boulder', 'Boulder'),
        ('Bradenton', 'Bradenton'),
        ('Bremerton', 'Bremerton'),
        ('Bridgeport', 'Bridgeport'),
        ('Brighton', 'Brighton'),
        ('Brownsville', 'Brownsville'),
        ('Bryan', 'Bryan'),
        ('Buffalo', 'Buffalo'),
        ('Burbank', 'Burbank'),
        ('Burlington', 'Burlington'),
        ('Cambridge', 'Cambridge'),
        ('Canton', 'Canton'),
        ('Cape Coral', 'Cape Coral'),
        ('Carrollton', 'Carrollton'),
        ('Cary', 'Cary'),
        ('Cathedral City', 'Cathedral City'),
        ('Cedar Rapids', 'Cedar Rapids'),
        ('Champaign', 'Champaign'),
        ('Chandler', 'Chandler'),
        ('Charleston', 'Charleston'),
        ('Charlotte', 'Charlotte'),
        ('Chattanooga', 'Chattanooga'),
        ('Chesapeake', 'Chesapeake'),
        ('Chicago', 'Chicago'),
        ('Chula Vista', 'Chula Vista'),
        ('Cincinnati', 'Cincinnati'),
        ('Clarke County', 'Clarke County'),
        ('Clarksville', 'Clarksville'),
        ('Clearwater', 'Clearwater'),
        ('Cleveland', 'Cleveland'),
        ('College Station', 'College Station'),
        ('Colorado Springs', 'Colorado Springs'),
        ('Columbia', 'Columbia'),
        ('Columbus', 'Columbus'),
        ('Concord', 'Concord'),
        ('Coral Springs', 'Coral Springs'),
        ('Corona', 'Corona'),
        ('Corpus Christi', 'Corpus Christi'),
        ('Costa Mesa', 'Costa Mesa'),
        ('Dallas', 'Dallas'),
        ('Daly City', 'Daly City'),
        ('Danbury', 'Danbury'),
        ('Davenport', 'Davenport'),
        ('Davidson County', 'Davidson County'),
        ('Dayton', 'Dayton'),
        ('Daytona Beach', 'Daytona Beach'),
        ('Deltona', 'Deltona'),
        ('Denton', 'Denton'),
        ('Denver', 'Denver'),
        ('Des Moines', 'Des Moines'),
        ('Detroit', 'Detroit'),
        ('Downey', 'Downey'),
        ('Duluth', 'Duluth'),
        ('Durham', 'Durham'),
        ('El Monte', 'El Monte'),
        ('El Paso', 'El Paso'),
        ('Elizabeth', 'Elizabeth'),
        ('Elk Grove', 'Elk Grove'),
        ('Elkhart', 'Elkhart'),
        ('Erie', 'Erie'),
        ('Escondido', 'Escondido'),
        ('Eugene', 'Eugene'),
        ('Evansville', 'Evansville'),
        ('Fairfield', 'Fairfield'),
        ('Fargo', 'Fargo'),
        ('Fayetteville', 'Fayetteville'),
        ('Fitchburg', 'Fitchburg'),
        ('Flint', 'Flint'),
        ('Fontana', 'Fontana'),
        ('Fort Collins', 'Fort Collins'),
        ('Fort Lauderdale', 'Fort Lauderdale'),
        ('Fort Smith', 'Fort Smith'),
        ('Fort Walton Beach', 'Fort Walton Beach'),
        ('Fort Wayne', 'Fort Wayne'),
        ('Fort Worth', 'Fort Worth'),
        ('Frederick', 'Frederick'),
        ('Fremont', 'Fremont'),
        ('Fresno', 'Fresno'),
        ('Fullerton', 'Fullerton'),
        ('Gainesville', 'Gainesville'),
        ('Garden Grove', 'Garden Grove'),
        ('Garland', 'Garland'),
        ('Gastonia', 'Gastonia'),
        ('Gilbert', 'Gilbert'),
        ('Glendale', 'Glendale'),
        ('Grand Prairie', 'Grand Prairie'),
        ('Grand Rapids', 'Grand Rapids'),
        ('Grayslake', 'Grayslake'),
        ('Green Bay', 'Green Bay'),
        ('GreenBay', 'GreenBay'),
        ('Greensboro', 'Greensboro'),
        ('Greenville', 'Greenville'),
        ('Gulfport-Biloxi', 'Gulfport-Biloxi'),
        ('Hagerstown', 'Hagerstown'),
        ('Hampton', 'Hampton'),
        ('Harlingen', 'Harlingen'),
        ('Harrisburg', 'Harrisburg'),
        ('Hartford', 'Hartford'),
        ('Havre de Grace', 'Havre de Grace'),
        ('Hayward', 'Hayward'),
        ('Hemet', 'Hemet'),
        ('Henderson', 'Henderson'),
        ('Hesperia', 'Hesperia'),
        ('Hialeah', 'Hialeah'),
        ('Hickory', 'Hickory'),
        ('High Point', 'High Point'),
        ('Hollywood', 'Hollywood'),
        ('Honolulu', 'Honolulu'),
        ('Houma', 'Houma'),
        ('Houston', 'Houston'),
        ('Howell', 'Howell'),
        ('Huntington', 'Huntington'),
        ('Huntington Beach', 'Huntington Beach'),
        ('Huntsville', 'Huntsville'),
        ('Independence', 'Independence'),
        ('Indianapolis', 'Indianapolis'),
        ('Inglewood', 'Inglewood'),
        ('Irvine', 'Irvine'),
        ('Irving', 'Irving'),
        ('Jackson', 'Jackson'),
        ('Jacksonville', 'Jacksonville'),
        ('Jefferson', 'Jefferson'),
        ('Jersey City', 'Jersey City'),
        ('Johnson City', 'Johnson City'),
        ('Joliet', 'Joliet'),
        ('Kailua', 'Kailua'),
        ('Kalamazoo', 'Kalamazoo'),
        ('Kaneohe', 'Kaneohe'),
        ('Kansas City', 'Kansas City'),
        ('Kennewick', 'Kennewick'),
        ('Kenosha', 'Kenosha'),
        ('Killeen', 'Killeen'),
        ('Kissimmee', 'Kissimmee'),
        ('Knoxville', 'Knoxville'),
        ('Lacey', 'Lacey'),
        ('Lafayette', 'Lafayette'),
        ('Lake Charles', 'Lake Charles'),
        ('Lakeland', 'Lakeland'),
        ('Lakewood', 'Lakewood'),
        ('Lancaster', 'Lancaster'),
        ('Lansing', 'Lansing'),
        ('Laredo', 'Laredo'),
        ('Las Cruces', 'Las Cruces'),
        ('Las Vegas', 'Las Vegas'),
        ('Layton', 'Layton'),
        ('Leominster', 'Leominster'),
        ('Lewisville', 'Lewisville'),
        ('Lexington', 'Lexington'),
        ('Lincoln', 'Lincoln'),
        ('Little Rock', 'Little Rock'),
        ('Long Beach', 'Long Beach'),
        ('Lorain', 'Lorain'),
        ('Los Angeles', 'Los Angeles'),
        ('Louisville', 'Louisville'),
        ('Lowell', 'Lowell'),
        ('Lubbock', 'Lubbock'),
        ('Macon', 'Macon'),
        ('Madison', 'Madison'),
        ('Manchester', 'Manchester'),
        ('Marina', 'Marina'),
        ('Marysville', 'Marysville'),
        ('McAllen', 'McAllen'),
        ('McHenry', 'McHenry'),
        ('Medford', 'Medford'),
        ('Melbourne', 'Melbourne'),
        ('Memphis', 'Memphis'),
        ('Merced', 'Merced'),
        ('Mesa', 'Mesa'),
        ('Mesquite', 'Mesquite'),
        ('Miami', 'Miami'),
        ('Milwaukee', 'Milwaukee'),
        ('Minneapolis', 'Minneapolis'),
        ('Miramar', 'Miramar'),
        ('Mission Viejo', 'Mission Viejo'),
        ('Mobile', 'Mobile'),
        ('Modesto', 'Modesto'),
        ('Monroe', 'Monroe'),
        ('Monterey', 'Monterey'),
        ('Montgomery', 'Montgomery'),
        ('Moreno Valley', 'Moreno Valley'),
        ('Murfreesboro', 'Murfreesboro'),
        ('Murrieta', 'Murrieta'),
        ('Muskegon', 'Muskegon'),
        ('Myrtle Beach', 'Myrtle Beach'),
        ('Naperville', 'Naperville'),
        ('Naples', 'Naples'),
        ('Nashua', 'Nashua'),
        ('Nashville', 'Nashville'),
        ('New Bedford', 'New Bedford'),
        ('New Haven', 'New Haven'),
        ('New London', 'New London'),
        ('New Orleans', 'New Orleans'),
        ('New York', 'New York'),
        ('New York City', 'New York City'),
        ('Newark', 'Newark'),
        ('Newburgh', 'Newburgh'),
        ('Newport News', 'Newport News'),
        ('Norfolk', 'Norfolk'),
        ('Normal', 'Normal'),
        ('Norman', 'Norman'),
        ('North Charleston', 'North Charleston'),
        ('North Las Vegas', 'North Las Vegas'),
        ('North Port', 'North Port'),
        ('Norwalk', 'Norwalk'),
        ('Norwich', 'Norwich'),
        ('Oakland', 'Oakland'),
        ('Ocala', 'Ocala'),
        ('Oceanside', 'Oceanside'),
        ('Odessa', 'Odessa'),
        ('Ogden', 'Ogden'),
        ('Oklahoma City', 'Oklahoma City'),
        ('Olathe', 'Olathe'),
        ('Olympia', 'Olympia'),
        ('Omaha', 'Omaha'),
        ('Ontario', 'Ontario'),
        ('Orange', 'Orange'),
        ('Orem', 'Orem'),
        ('Orlando', 'Orlando'),
        ('Overland Park', 'Overland Park'),
        ('Oxnard', 'Oxnard'),
        ('Palm Bay', 'Palm Bay'),
        ('Palm Springs', 'Palm Springs'),
        ('Palmdale', 'Palmdale'),
        ('Panama City', 'Panama City'),
        ('Pasadena', 'Pasadena'),
        ('Paterson', 'Paterson'),
        ('Pembroke Pines', 'Pembroke Pines'),
        ('Pensacola', 'Pensacola'),
        ('Peoria', 'Peoria'),
        ('Philadelphia', 'Philadelphia'),
        ('Phoenix', 'Phoenix'),
        ('Pittsburgh', 'Pittsburgh'),
        ('Plano', 'Plano'),
        ('Pomona', 'Pomona'),
        ('Pompano Beach', 'Pompano Beach'),
        ('Port Arthur', 'Port Arthur'),
        ('Port Orange', 'Port Orange'),
        ('Port Saint Lucie', 'Port Saint Lucie'),
        ('Port St. Lucie', 'Port St. Lucie'),
        ('Portland', 'Portland'),
        ('Portsmouth', 'Portsmouth'),
        ('Poughkeepsie', 'Poughkeepsie'),
        ('Providence', 'Providence'),
        ('Provo', 'Provo'),
        ('Pueblo', 'Pueblo'),
        ('Punta Gorda', 'Punta Gorda'),
        ('Racine', 'Racine'),
        ('Raleigh', 'Raleigh'),
        ('Rancho Cucamonga', 'Rancho Cucamonga'),
        ('Reading', 'Reading'),
        ('Redding', 'Redding'),
        ('Reno', 'Reno'),
        ('Richland', 'Richland'),
        ('Richmond', 'Richmond'),
        ('Richmond County', 'Richmond County'),
        ('Riverside', 'Riverside'),
        ('Roanoke', 'Roanoke'),
        ('Rochester', 'Rochester'),
        ('Rockford', 'Rockford'),
        ('Roseville', 'Roseville'),
        ('Round Lake Beach', 'Round Lake Beach'),
        ('Sacramento', 'Sacramento'),
        ('Saginaw', 'Saginaw'),
        ('Saint Louis', 'Saint Louis'),
        ('Saint Paul', 'Saint Paul'),
        ('Saint Petersburg', 'Saint Petersburg'),
        ('Salem', 'Salem'),
        ('Salinas', 'Salinas'),
        ('Salt Lake City', 'Salt Lake City'),
        ('San Antonio', 'San Antonio'),
        ('San Bernardino', 'San Bernardino'),
        ('San Buenaventura', 'San Buenaventura'),
        ('San Diego', 'San Diego'),
        ('San Francisco', 'San Francisco'),
        ('San Jose', 'San Jose'),
        ('Santa Ana', 'Santa Ana'),
        ('Santa Barbara', 'Santa Barbara'),
        ('Santa Clara', 'Santa Clara'),
        ('Santa Clarita', 'Santa Clarita'),
        ('Santa Cruz', 'Santa Cruz'),
        ('Santa Maria', 'Santa Maria'),
        ('Santa Rosa', 'Santa Rosa'),
        ('Sarasota', 'Sarasota'),
        ('Savannah', 'Savannah'),
        ('Scottsdale', 'Scottsdale'),
        ('Scranton', 'Scranton'),
        ('Seaside', 'Seaside'),
        ('Seattle', 'Seattle'),
        ('Sebastian', 'Sebastian'),
        ('Shreveport', 'Shreveport'),
        ('Simi Valley', 'Simi Valley'),
        ('Sioux City', 'Sioux City'),
        ('Sioux Falls', 'Sioux Falls'),
        ('South Bend', 'South Bend'),
        ('South Lyon', 'South Lyon'),
        ('Spartanburg', 'Spartanburg'),
        ('Spokane', 'Spokane'),
        ('Springdale', 'Springdale'),
        ('Springfield', 'Springfield'),
        ('St. Louis', 'St. Louis'),
        ('St. Paul', 'St. Paul'),
        ('St. Petersburg', 'St. Petersburg'),
        ('Stamford', 'Stamford'),
        ('Sterling Heights', 'Sterling Heights'),
        ('Stockton', 'Stockton'),
        ('Sunnyvale', 'Sunnyvale'),
        ('Syracuse', 'Syracuse'),
        ('Tacoma', 'Tacoma'),
        ('Tallahassee', 'Tallahassee'),
        ('Tampa', 'Tampa'),
        ('Temecula', 'Temecula'),
        ('Tempe', 'Tempe'),
        ('Thornton', 'Thornton'),
        ('Thousand Oaks', 'Thousand Oaks'),
        ('Toledo', 'Toledo'),
        ('Topeka', 'Topeka'),
        ('Torrance', 'Torrance'),
        ('Trenton', 'Trenton'),
        ('Tucson', 'Tucson'),
        ('Tulsa', 'Tulsa'),
        ('Tuscaloosa', 'Tuscaloosa'),
        ('Tyler', 'Tyler'),
        ('Utica', 'Utica'),
        ('Vallejo', 'Vallejo'),
        ('Vancouver', 'Vancouver'),
        ('Vero Beach', 'Vero Beach'),
        ('Victorville', 'Victorville'),
        ('Virginia Beach', 'Virginia Beach'),
        ('Visalia', 'Visalia'),
        ('Waco', 'Waco'),
        ('Warren', 'Warren'),
        ('Washington', 'Washington'),
        ('Waterbury', 'Waterbury'),
        ('Waterloo', 'Waterloo'),
        ('West Covina', 'West Covina'),
        ('West Valley City', 'West Valley City'),
        ('Westminster', 'Westminster'),
        ('Wichita', 'Wichita'),
        ('Wilmington', 'Wilmington'),
        ('Winston', 'Winston'),
        ('Winter Haven', 'Winter Haven'),
        ('Worcester', 'Worcester'),
        ('Yakima', 'Yakima'),
        ('Yonkers', 'Yonkers'),
        ('York', 'York'),
        ('Youngstown', 'Youngstown'),
        ('Other', 'Other'),
    )

    STATUS = (
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Declined', 'Declined'),
        ('Inactive', 'Inactive'),
        )

    user = models.ForeignKey(User, unique=True)
    status = models.CharField(choices=STATUS, max_length=200, blank=True)
    job_title = models.CharField(max_length=200)
    location = models.CharField(choices=LOCATION, max_length=200)
    company = models.CharField(max_length=200)
    link = models.URLField()
    linkedin = models.URLField()
    twitter = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    bio = models.TextField()
    image = models.ImageField(upload_to='images/%Y%m%d', null=True)
    team = models.CharField(max_length=200)
    events = ArrayField(models.CharField(max_length=200), blank=True)
    activities = ArrayField(models.CharField(max_length=200))
    mentorship = ArrayField(models.CharField(max_length=200))
    panel = models.BooleanField(default=False)
    moderator = models.BooleanField(default=False)
    referal = models.CharField(max_length=200, blank=True)
    referal_email = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.user)