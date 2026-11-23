import re

from django.db import models


class ProfileInfo(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="الاسم الكامل")
    title = models.CharField(max_length=200, verbose_name="المسمى الوظيفي")
    bio = models.TextField(verbose_name="نبذة عني")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True, verbose_name="الصورة الشخصية")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=30, blank=True, verbose_name="رقم الهاتف / واتساب")
    location = models.CharField(max_length=150, blank=True, verbose_name="الموقع")
    github_url = models.URLField(blank=True, verbose_name="رابط GitHub")
    linkedin_url = models.URLField(blank=True, verbose_name="رابط LinkedIn")
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True, verbose_name="ملف السيرة الذاتية (PDF)")

    def get_whatsapp_number(self):
        if not self.phone:
            return ''
        digits = ''.join(ch for ch in self.phone if ch.isdigit())
        if digits.startswith('01') and len(digits) == 11:
            return '2' + digits
        if digits.startswith('00'):
            return digits[2:]
        return digits
    @property
    def whatsapp_number(self):
        if not self.phone:
            return ""
        # إزالة أي مسافات أو علامات + أو شرطات
        digits = re.sub(r'\D', '', self.phone)
        # إذا كان الرقم مصرياً يبدأ بـ 01 (11 رقم) نحوله ليبدأ بـ 20
    class Meta:
        verbose_name = "المعلومات الشخصية"
        verbose_name_plural = "المعلومات الشخصية"

    def __str__(self):
        return self.full_name


class Service(models.Model):
    title = models.CharField(max_length=150, verbose_name="اسم الخدمة")
    description = models.TextField(verbose_name="وصف الخدمة")
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="مثال: fa-solid fa-code أو fa-solid fa-robot",
        verbose_name="أيقونة (FontAwesome)"
    )
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="صورة الخدمة (اختياري)")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتيب العرض")
    is_active = models.BooleanField(default=True, verbose_name="مفعّلة")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "خدمة"
        verbose_name_plural = "الخدمات"

    def __str__(self):
        return self.title


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend & APIs'),
        ('mobile', 'Mobile Apps (Flutter)'),
        ('ai', 'AI & Data Science'),
        ('fullstack', 'Full-Stack Web'),
    ]

    title = models.CharField(max_length=200, verbose_name="اسم المشروع")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="الرابط المختصر (Slug)")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='fullstack', verbose_name="التصنيف")
    short_description = models.CharField(max_length=300, verbose_name="وصف مختصر للكارد")
    description = models.TextField(verbose_name="الوصف الكامل للمشروع")
    execution_time = models.CharField(
        max_length=100,
        help_text="مثال: 3 أسابيع أو شهرين",
        verbose_name="وقت / مدة التنفيذ"
    )
    technologies = models.CharField(
        max_length=250,
        help_text="افصل بين التقنيات بفاصلة، مثال: Python, Django, Flutter, PostgreSQL",
        verbose_name="التقنيات المستخدمة"
    )
    main_image = models.ImageField(upload_to='projects/main/', verbose_name="الصورة الرئيسية للمشروع")
    live_url = models.URLField(blank=True, verbose_name="رابط المعاينة الحية")
    github_url = models.URLField(blank=True, verbose_name="رابط الكود (GitHub)")
    created_at = models.DateField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    is_featured = models.BooleanField(default=False, verbose_name="مشروع مميز")

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "مشروع"
        verbose_name_plural = "سابقة الأعمال (المشاريع)"

    def __str__(self):
        return self.title

    def get_tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name="المشروع")
    image = models.ImageField(upload_to='projects/gallery/', verbose_name="صورة إضافية")
    caption = models.CharField(max_length=150, blank=True, verbose_name="وصف الصورة (اختياري)")

    class Meta:
        verbose_name = "صورة مشروع"
        verbose_name_plural = "صور المشروع"

    def __str__(self):
        return f"صورة لـ {self.project.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150, verbose_name="الاسم")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    subject = models.CharField(max_length=200, verbose_name="الموضوع")
    message = models.TextField(verbose_name="الرسالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="وقت الإرسال")
    is_read = models.BooleanField(default=False, verbose_name="تمت القراءة")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "رسالة تواصل"
        verbose_name_plural = "رسائل التواصل"

    def __str__(self):
        return f"{self.name} - {self.subject}"