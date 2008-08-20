from django.db import models
from django.contrib.auth.models import User
from podcast.managers import EpisodeManager


class Category(models.Model):
    """Category model."""
    NAME_CHOICES = (
        ('Arts', (
                ('Design', 'Design'),
                ('Fashion & Beauty', 'Fashion & Beauty'),
                ('Food', 'Food'),
                ('Literature', 'Literature'),
                ('Performing Arts', 'Performing Arts'),
                ('Visual Arts', 'Visual Arts'),
            )
        ),
        ('Business', (
                ('Business News', 'Business News'),
                ('Careers', 'Careers'),
                ('Investing', 'Investing'),
                ('Management & Marketing', 'Management & Marketing'),
                ('Shopping', 'Shopping'),
            )
        ),
        ('Comdey', 'Comedy'),
        ('Education', (
                ('Education Technology', 'Education Technology'),
                ('Higher Education', 'Higher Education'),
                ('K-12', 'K-12'),
                ('Language Courses', 'Language Courses'),
                ('Training', 'Training'),
            )
        ),
        ('Education', (
                ('Education Technology', 'Education Technology'),
                ('Higher Education', 'Higher Education'),
                ('K-12', 'K-12'),
                ('Language Courses', 'Language Courses'),
                ('Training', 'Training'),
            )
        ),
        ('Games & Hobbies', (
                ('Automotive', 'Automotive'),
                ('Aviation', 'Aviation'),
                ('Hobbies', 'Hobbies'),
                ('Other Games', 'Other Games'),
                ('Video Games', 'Video Games'),
            )
        ),
        ('Government & Organizations', (
                ('Local', 'Local'),
                ('National', 'National'),
                ('Non-Profit', 'Non-Profit'),
                ('Regional', 'Regional'),
            )
        ),
        ('Health', (
                ('Alternative Health', 'Alternative Health'),
                ('Fitness & Nutrition', 'Fitness & Nutrition'),
                ('Self-Help', 'Self-Help'),
                ('Sexuality', 'Sexuality'),
            )
        ),
        ('Kids & Family', 'Kids & Family'),
        ('Music', 'Music'),
        ('News & Politics', 'News & Politics'),
        ('Religion & Spirituality', (
                ('Buddhism', 'Buddhism'),
                ('Christianity', 'Christianity'),
                ('Hinduism', 'Hinduism'),
                ('Islam', 'Islam'),
                ('Judaism', 'Judaism'),
                ('Other', 'Other'),
                ('Spirituality', 'Spirituality'),
            )
        ),
        ('Science & Medicine', (
                ('Medicine', 'Medicine'),
                ('Natural Sciences', 'Natural Sciences'),
                ('Social Sciences', 'Social Sciences'),
            )
        ),
        ('Society & Culture', (
                ('History', 'History'),
                ('Personal Journals', 'Personal Journals'),
                ('Philosophy', 'Philosophy'),
                ('Places & Travel', 'Places & Travel'),
            )
        ),
        ('Sports & Recreation', (
                ('Amateur', 'Amateur'),
                ('College & High School', 'College & High School'),
                ('Outdoor', 'Outdoor'),
                ('Professional', 'Professional'),
            )
        ),
        ('Technology', (
                ('Gadgets', 'Gadgets'),
                ('Tech News', 'Tech News'),
                ('Podcasting', 'Podcasting'),
                ('Software How-To', 'Software How-To'),
            )
        ),
        ('TV & Film', 'TV & Film'),
    )
    name = models.CharField(max_length=26, choices=NAME_CHOICES)
    slug = models.SlugField(unique=True, help_text="Auto-generated, so don't worry about this.")

    class Meta:
        ordering = ['name']
        verbose_name_plural = "categories"

    def __unicode__(self):
        return u'%s' % (self.name)


class Show(models.Model):
    """Show model."""
    EXPLICIT_CHOICES = (
      ('yes', 'Yes'),
      ('no', 'No'),
      ('clean', 'Clean'),
    )
    organization = models.CharField(max_length=255, help_text="Name of the organization or company producing your podcast.")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Auto-generated, so don't worry about this.")
    subtitle = models.CharField(max_length=255, help_text="Displays best if only a few words long like a tagline.")
    language = models.CharField(max_length=5, default="en-us", help_text="Default is American English. See <a href=\"http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes\">ISO 639-1</a> and <a href=\"http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements\">ISO 3166-1</a> for more language codes.")
    author = models.ForeignKey(User)
    description = models.TextField(help_text="Describe subject matter, media format, episode schedule and other relevant information. Incorporate some keywords. Neither HTML nor Markdown is accepted.")
    summary = models.TextField(help_text="iTunes-specific description; allows 4,000 characters. Description will be used if summary is blank. Neither HTML nor Markdown is accepted.", blank=True)
    image = models.ImageField(upload_to="podcasts/img/", help_text="An attractive, original square JPEG (.jpg) or PNG (.png) image of 600x600 pixels; will be scaled down to 50x50 pixels at smallest.")
    player = models.FileField(upload_to="podcasts/", help_text="An optional Adobe Shockwave Flash (.swf) video player that loads external videos, for inclusion in a Google video sitemap.", blank=True)
    category = models.ManyToManyField(Category, help_text="Having a category makes the podcast appear in more places in iTunes and is more likely to be found by users.")
    keywords = models.CharField(max_length=255, help_text="A comma-separated list of words for iTunes searches, up to 12; perhaps include misspellings of title.")
    explicit = models.CharField(max_length=255, default="no", choices=EXPLICIT_CHOICES, help_text="\"Clean\" will put the clean iTunes graphic by it.")
    block = models.BooleanField(default=False, help_text="Check to temporarily block this show from iTunes.")
    link = models.URLField(help_text="URL of the main website or the podcast section of the main website.")
    redirect = models.URLField(help_text="URL of the new podcast feed; must continue old feed for at least two weeks. Write a 301 redirect for old feed, too.", blank=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return u'%s' % (self.title)


class Episode(models.Model):
    """Episode model."""
    SECONDS_CHOICES = tuple(('%02d' % x, str(x)) for x in range(60))
    MIME_CHOICES = (
      ('audio/mpeg', '.mp3 (audio)'),
      ('audio/x-m4a', '.m4a (audio)'),
      ('video/mp4', '.mp4 (audio or video)'),
      ('video/x-m4v', '.m4v (video)'),
      ('video/quicktime', '.mov (video)'),
      ('application/pdf', '.pdf (document)'),
    )
    EXPLICIT_CHOICES = (
      ('yes', 'Yes'),
      ('no', 'No'),
      ('clean', 'Clean'),
    )
    show = models.ForeignKey(Show)
    title = models.CharField(max_length=255, help_text="Make it specific, but avoid explicit language. Limit to 100 characters for inclusion in a Google video sitemap.")
    slug = models.SlugField(unique=True, help_text="Auto-generated, so don't worry about this.")
    subtitle = models.CharField(max_length=255, help_text="Displays best if only a few words long like a tagline.")
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, help_text="Written in HH:MM:SS military time")
    description = models.TextField(help_text="Neither HTML nor Markdown is accepted. Avoid explicit language. Limitd to 2,048 characters for inclusion in a Google video sitemap.")
    summary = models.TextField(help_text="iTunes-specific description; allows 4,000 characters. Description will be used if summary is blank. Neither HTML nor Markdown is accepted.", blank=True)
    minutes = models.PositiveIntegerField()
    seconds = models.CharField(max_length=2, choices=SECONDS_CHOICES)
    file = models.FileField(upload_to="postcasts/mov/", help_text="Must be less than or equal to 30 MB for a Google video sitemap.")
    image = models.ImageField(upload_to="podcasts/img/", help_text="A thumbnail screenshot of a scene from the video for inclusion in a Google video sitemap. Individual podcast artwork must be in the file's metadata!", blank=True)
    mime = models.CharField("Format", max_length=255, choices=MIME_CHOICES, default="video/mp4")
    keywords = models.CharField(max_length=255, help_text="A comma-separated list of words for iTunes searches, up to 12; perhaps include misspellings.")
    explicit = models.CharField(max_length=255, default="no", choices=EXPLICIT_CHOICES, help_text="\"Clean\" will put the clean iTunes graphic by it.")
    block = models.BooleanField(help_text="Check to block this episode from iTunes because its content might cause the entire show to be removed from iTunes.", default=False)
    embed = models.BooleanField(help_text="Check to allow Google to embed video in search results on <a href=\"http://video.google.com\">Google Video</a>. Note: Will only work if .swf player is uploaded in respective Show.", default=True)
    published = models.BooleanField("Publish live?", default=True)
    objects = EpisodeManager()

    class Meta:
        ordering = ['-date', 'author', 'title']

    def __unicode__(self):
        return u'%s' % (self.title)

    def seconds_total(self):
        try:
            return (((float(self.minutes)) * 60) + (float(self.seconds)))
        except:
            return 0