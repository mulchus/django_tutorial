import pytest


@pytest.mark.django_db
def test_exist_user(django_user_model):
    django_user_model.objects.create_user(username='testuser', password='testpassword')
    assert len(django_user_model.objects.all()) == 1
    user = django_user_model.objects.get(username='testuser')
    assert user.pk is not None
    assert user.username == 'testuser'


def test_non_exist_user(django_user_model):
    with pytest.raises(django_user_model.DoesNotExist):
        django_user_model.objects.get(username='testuser')
