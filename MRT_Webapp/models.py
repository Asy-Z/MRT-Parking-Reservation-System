from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, primary_key=True)  
    password = models.CharField(max_length=128)  
    USERTYPE = [
        ('Administrator', 'Administrator'),
        ('Commuter', 'Commuter'),
    ]
    role = models.CharField(max_length=50, choices=USERTYPE)

class Commuter(models.Model):
    CommID = models.AutoField(primary_key=True)
    CommName = models.CharField(max_length=50)
    CommEmail = models.EmailField(max_length=50, unique=True)
    CommPass = models.CharField(max_length=50)

class Administrator(models.Model):
    AdminID = models.AutoField(primary_key=True)
    AdminName = models.CharField(max_length=50)
    AdminEmail = models.EmailField(max_length=50, unique=True)
    AdminPass = models.CharField(max_length=50)
    
class Payment(models.Model):
    PayID = models.AutoField(primary_key=True)
    CommID = models.ForeignKey(Commuter, on_delete=models.CASCADE)
    
    PayMethod = [
        ('QR Code', 'QR Code'),
        ('Account Transfer', 'Account Transfer'),
    ]
    
    Method = models.CharField(max_length=50, choices=PayMethod)
    Amount = models.IntegerField()
    
class Parking(models.Model):
        
    ParkID = models.CharField(max_length=50, primary_key=True,)    
    
    MRT = [
    ("Sungai Buloh", "Sungai Buloh"),
    ("Kampung Selamat", "Kampung Selamat"),
    ("Kwasa Damansara", "Kwasa Damansara"),
    ("Kwasa Sentral", "Kwasa Sentral"),
    ("Kota Damansara", "Kota Damansara"),
    ("Surian", "Surian"),
    ("Mutiara Damansara", "Mutiara Damansara"),
    ("Bandar Utama", "Bandar Utama"),
    ("TTDI", "TTDI"),
    ("Phileo Damansara", "Phileo Damansara"),
    ("Pusat Bandar Damansara", "Pusat Bandar Damansara"),
    ("Semantan", "Semantan"),
    ("Muzium Negara", "Muzium Negara"),
    ("Pasar Seni", "Pasar Seni"),
    ("Merdeka", "Merdeka"),
    ("Bukit Bintang", "Bukit Bintang"),
    ("Tun Razak Exchange", "Tun Razak Exchange"),
    ("Cochrane", "Cochrane"),
    ("Maluri", "Maluri"),
    ("Taman Pertama", "Taman Pertama"),
    ("Taman Midah", "Taman Midah"),
    ("Taman Mutiara", "Taman Mutiara"),
    ("Taman Connaught", "Taman Connaught"),
    ("Taman Suntex", "Taman Suntex"),
    ("Sri Raya", "Sri Raya"),
    ("Bandar Tun Hussein Onn", "Bandar Tun Hussein Onn"),
    ("Batu 11 Cheras", "Batu 11 Cheras"),
    ("Bukit Dukung", "Bukit Dukung"),
    ("Sungai Jernih", "Sungai Jernih"),
    ("Stadium Kajang", "Stadium Kajang"),
    ("Kajang", "Kajang"),
    ("Damansara Damai", "Damansara Damai"),
    ("Sri Damansara Barat", "Sri Damansara Barat"),
    ("Sri Damansara Sentral", "Sri Damansara Sentral"),
    ("Sri Damansara Timur", "Sri Damansara Timur"),
    ("Metro Prima", "Metro Prima"),
    ("Kepong Baru", "Kepong Baru"),
    ("Jinjang", "Jinjang"),
    ("Sri Delima", "Sri Delima"),
    ("Kentonmen", "Kentonmen"),
    ("Jalan Ipoh", "Jalan Ipoh"),
    ("Sentul Barat", "Sentul Barat"),
    ("Titiwangsa", "Titiwangsa"),
    ("Hospital Kuala Lumpur", "Hospital Kuala Lumpur"),
    ("Raja Uda", "Raja Uda"),
    ("Ampang Park", "Ampang Park"),
    ("Persiaran KLCC", "Persiaran KLCC"),
    ("Conlay", "Conlay"),
    ("Chan Sow Lin", "Chan Sow Lin"),
    ("Kuchai", "Kuchai"),
    ("Taman Naga Emas", "Taman Naga Emas"),
    ("Sungai Besi", "Sungai Besi"),
    ("Serdang Raya Utara", "Serdang Raya Utara"),
    ("Serdang Raya Selatan", "Serdang Raya Selatan"),
    ("Serdang Jaya", "Serdang Jaya"),
    ("UPM", "UPM"),
    ("Taman Equine", "Taman Equine"),
    ("Putra Permai", "Putra Permai"),
    ("16 Sierra", "16 Sierra"),
    ("Cyberjaya Utara", "Cyberjaya Utara"),
    ("Cyberjaya City Centre", "Cyberjaya City Centre"),
    ("Putrajaya Sentral", "Putrajaya Sentral"),
]
    
    Station = models.CharField(max_length=50, choices=MRT)
    
    tingkat = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
    ]
    
    Level = models.CharField(max_length=50, choices=tingkat)
    
    ParkBox = [
        (i, f'Box {i}') for i in range(1, 31)
    ]
    
    BoxNo = models.CharField(max_length=50, choices=ParkBox)
    
    kondisi = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Under Maintenance', 'Under Maintenance')
    ]
    
    Status = models.CharField(max_length=50, choices=kondisi, default='Available')
    
    def save(self, *args, **kwargs):
        self.ParkID = f"{self.Station}-{self.Level}-{self.BoxNo}"
        super(Parking, self).save(*args, **kwargs)
    
class Reservation(models.Model):
    ReserveID = models.AutoField(primary_key=True)
    CommID =  models.ForeignKey(Commuter, on_delete=models.CASCADE)
    ParkID = models.ForeignKey(Parking, on_delete=models.CASCADE)
    PayID = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    PlateNo = models.CharField(max_length=50)
    DateTimeStart = models.DateTimeField(null = True, blank = True)
    DateTimeEnd = models.DateTimeField(null = True, blank = True)
    
    
    
    
    