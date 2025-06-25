from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from django.utils.text import slugify


class HomePage(Page):
    subpage_types = ['home.BlogIndexPage']
    template = "home/home_page.html"
    content_panels = Page.content_panels


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPage(Page):
    parent_page_types = ['home.BlogIndexPage']
    subpage_types = []
    template = "home/blog_page.html"
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    category = models.ForeignKey(
        'home.Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blog_posts'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('main_image'),
        FieldPanel('category'),
        FieldPanel('tags'),
    ]


class BlogIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.BlogPage']
    template = "home/blog_index_page.html"
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['posts'] = BlogPage.objects.live().descendant_of(self).order_by('-date')
        return context
