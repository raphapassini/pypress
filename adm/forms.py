from django import forms
from treemenus.models import Menu, MenuItem
from core.models import Category, Page
from timezone_field import TimeZoneFormField


class GeneralConfig(forms.Form):
    site_title = forms.CharField(label='Site Title')
    site_desc = forms.CharField(label='Site Description')
    site_url = forms.URLField(label='Site URL')
    site_email = forms.EmailField(label='Site Email',
                                  help_text='This field is only used by '
                                  'system to notify purposes. Like new users.')
    timezone = TimeZoneFormField(label='Timezone')
    register_open = forms.BooleanField(label='Membership - Anyone can '
                                       'register', initial=False,
                                       required=False)


class WriteConfig(forms.Form):
    default_category = forms.ChoiceField(label="Default Category", choices=[])
    github_repository = forms.URLField(
        required=False,
        label='Github Repository',
        help_text='A URL to a git repository '
        'containing the .rst or .md files that will be converted to entries')

    def __init__(self, *args, **kwargs):
        super(WriteConfig, self).__init__(*args, **kwargs)
        qs = Category.objects.all()
        self.fields['default_category'].choices = [(x.pk, x.name) for x in qs]


class ReadConfig(forms.Form):
    HOMEPAGE_CHOICES = [
        ('recent_entries', 'Recent Entries'),
        ('static_page', 'Static Page')
    ]

    homepage = forms.ChoiceField(
        initial='recent_entries',
        choices=HOMEPAGE_CHOICES, widget=forms.RadioSelect())
    homepage_choices = forms.ChoiceField(choices=[])
    entries_per_page = forms.IntegerField(
        initial=10,
        help_text="Numbers of entries per page")

    def __init__(self, *args, **kwargs):
        super(ReadConfig, self).__init__(*args, **kwargs)
        qs = Page.objects.all()
        self.fields['homepage_choices'].choices = [(x.pk, x.title) for x in qs]


class CommentConfig(forms.Form):
    DEFAULT_ENTRY_OPTIONS = [
        ('allow_pingbacks', 'Allow notifications from other blogs'),
        ('allow_comments', 'Allow users to comment on your new entries')
    ]

    COMMENT_OPTIONS = [
        ('comment_author_name_email_required', 'Comments author have to '
         'fill name and email'),
        ('comment_author_must_register', 'Users must register before comment'),
        ('show_avatar', 'Show author avatar in comments')
    ]

    COMMENT_SHOW_OPTIONS = [
        ('older', 'Show the older comments first'),
        ('newer', 'Show the newer comments first'),
    ]

    COMMENT_SEND_ME_EMAIL_WHEN = [
        ('new_comment', 'Someone publish a comment'),
        ('wait_moderation', 'A comment needs to be moderate')
    ]

    COMMENT_BEFORE_SHOW_OPTIONS = [
        ('manual_approval', 'Every comment has to be manually approved'),
        ('author_was_approved', 'The author already has a comment approved')
    ]

    default_entry_options = forms.MultipleChoiceField(
        required=False, choices=DEFAULT_ENTRY_OPTIONS,
        widget=forms.CheckboxSelectMultiple)
    comment_options = forms.MultipleChoiceField(
        required=False, choices=COMMENT_OPTIONS,
        widget=forms.CheckboxSelectMultiple)
    days_autoclose_comments = forms.IntegerField(
        label="Auto close comments on entries older than X days",
        required=False, initial=15)
    comment_show_options = forms.ChoiceField(
        label='Show comments in this order', initial='older', required=False,
        choices=COMMENT_SHOW_OPTIONS)
    slipt_comments = forms.CharField(
        label="How many comments per page",
        help_text="If you leave this field blank, all comments will be show.",
        required=False)
    comment_send_me_email_when = forms.MultipleChoiceField(
        required=False, choices=COMMENT_SEND_ME_EMAIL_WHEN,
        widget=forms.CheckboxSelectMultiple)
    before_show_comment = forms.MultipleChoiceField(
        required=False, choices=COMMENT_BEFORE_SHOW_OPTIONS,
        widget=forms.CheckboxSelectMultiple)
    comment_moderation = forms.CharField(
        required=False, label="Comments containing any of this words, IP, "
        "name, URL or Email will be added to moderation queue",
        help_text="One word, IP, name, URL or Email PER LINE!",
        widget=forms.Textarea)
    comment_blacklist = forms.CharField(
        required=False, label="Comments containing any of this words, IP, "
        "name, URL or Email will be marked as spam",
        help_text="One word, IP, name, URL or Email PER LINE!",
        widget=forms.Textarea)


class CreateMenuForm(forms.ModelForm):
    class Meta:
        model = Menu


class MenuSelectForm(forms.Form):
    menu = forms.ChoiceField(label="Menu", choices=[],
                             required=False)

    def __init__(self, *args, **kwargs):
        super(MenuSelectForm, self).__init__(*args, **kwargs)
        self.fields['menu'].choices = [(x.pk, x.name) for x in
                                       Menu.objects.all()]
        self.fields['menu'].choices.insert(0, ('', '---------'))


class PageSelectForm(forms.Form):
    page_type = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(attrs={'class': '__menu_type'}),
        initial='page')
    page = forms.MultipleChoiceField(
        required=False, choices=[], label='',)

    def __init__(self, *args, **kwargs):
        super(PageSelectForm, self).__init__(*args, **kwargs)
        self.fields['page'].choices = [(x.pk, x.title) for x in
                                       Page.objects.all()]


class CategorySelectForm(forms.Form):
    category_type = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(attrs={'class': '__menu_type'}),
        initial='category')
    category = forms.MultipleChoiceField(
        required=False, choices=[], label='',)

    def __init__(self, *args, **kwargs):
        super(CategorySelectForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [(x.pk, x.name) for x in
                                           Category.objects.all()]


class ExternalLinkForm(forms.Form):
    link_type = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(attrs={'class': '__menu_type'}),
        initial='link')
    URL = forms.URLField()
    text = forms.CharField(label='Link text')


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
