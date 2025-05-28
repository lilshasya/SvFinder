from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class AdminSistem(models.Model):
    id_admin = models.CharField(max_length=30, primary_key=True)
    nama_admin = models.CharField(max_length=255)
    email_admin =  models.EmailField(max_length=255)
    no_admin = models.CharField(max_length=11)
    katalaluan_admin = models.CharField(max_length=255)

class Pelajar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id_pelajar = models.CharField(max_length=30, primary_key=True)
    nama_pelajar = models.CharField(max_length=255)
    email_pelajar = models.EmailField(max_length=255)
    no_pelajar = models.CharField(max_length=15)
    katalaluan_pelajar = models.CharField(max_length=30)
    program_pelajar = models.CharField(max_length=255)
    gambar_pelajar = models.ImageField(upload_to='pelajar/', null=True, blank=True)  # <-- Added here
    id_admin = models.ForeignKey('AdminSistem', on_delete=models.CASCADE, null=True, blank=True)

    

class Penyelia(models.Model):
    id_penyelia = models.CharField(max_length=30, primary_key=True)
    nama_penyelia = models.CharField(max_length=255)
    email_penyelia = models.EmailField(max_length=255)
    no_penyelia = models.CharField(max_length=15)
    category_penyelia = models.CharField(max_length=255)  # Changed from 'program_penyelia' to 'category_penyelia'
    katalaluan_penyelia = models.CharField(max_length=255)
    kepakaran_penyelia = models.CharField(max_length=255)
    gambar_penyelia = models.ImageField(upload_to='penyelia/', null=True, blank=True)
    id_admin = models.ForeignKey('AdminSistem', on_delete=models.CASCADE, null=True, blank=True)
    bilik_penyelia = models.CharField(max_length=255, null=True, blank=True)  # Make it nullable
    bio_penyelia = models.CharField(max_length=3000, null=True, blank=True)
    academic_penyelia = models.CharField(max_length=255, null=True, blank=True)  # New field for academic info


class Permohonan(models.Model):
    id_permohonan = models.CharField(max_length=30 , primary_key=True)
    id_pelajar = models.ForeignKey(Pelajar, on_delete=models.CASCADE)
    id_penyelia = models.ForeignKey (Penyelia, on_delete=models.CASCADE)  # fixed typo here
    tarikh_permohonan= models.DateField ()
    sinopsis = models.FileField(upload_to='sinopsis/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])])   


class Status(models.Model):
    id_status = models.CharField(max_length=30 , primary_key=True)
    id_permohonan = models.ForeignKey(Permohonan, on_delete=models.CASCADE)
    status = models.CharField(max_length=70)
    ulasan = models.CharField(max_length=3000)
    tarikh_kemaskini_status = models.DateField()

class Laporan(models.Model):
    id_laporan = models.CharField(max_length=30 , primary_key=True)
    bilangan_permohonan = models.IntegerField()  # fixed typo here: "pemohonan" to "permohonan"
    bilangan_diluluskan = models.IntegerField()
    bilangan_ditolak = models.IntegerField()
    id_admin = models.ForeignKey(AdminSistem, on_delete=models.CASCADE)
