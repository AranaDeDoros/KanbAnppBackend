import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from projects.models import Project

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def d(db):
    owner = User.objects.create_user(username="owner", password="pass")
    member = User.objects.create_user(username="member", password="pass")
    outsider = User.objects.create_user(username="outsider", password="pass")
    return owner, member, outsider

@pytest.fixture
def projects(users):
    owner, member, _ = users
    p1 = Project.objects.create(name="Owner Project", description="", owner=owner)
    p2 = Project.objects.create(name="Member Project", description="", owner=User.objects.create_user(username="other", password="pass"))
    p2.members.add(member)
    p3 = Project.objects.create(name="Other Project", description="", owner=User.objects.create_user(username="someone", password="pass"))
    return p1, p2, p3

@pytest.fixture
def auth_client(api_client, users):
    owner, member, outsider = users
    def get_client(user):
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return api_client
    return get_client

# ---------------------------
# Tests get_queryset
# ---------------------------

@pytest.mark.django_db
def test_owner_sees_own_projects(auth_client, projects, users):
    client = auth_client(users[0])  # owner
    response = client.get("/projects/")
    ids = [p["id"] for p in response.json()]
    assert projects[0].id in ids
    assert projects[1].id not in ids
    assert projects[2].id not in ids

@pytest.mark.django_db
def test_member_sees_member_projects(auth_client, projects, users):
    client = auth_client(users[1])  # member
    response = client.get("/projects/")
    ids = [p["id"] for p in response.json()]
    assert projects[1].id in ids
    assert projects[0].id not in ids
    assert projects[2].id not in ids

@pytest.mark.django_db
def test_outsider_sees_nothing(auth_client, projects, users):
    client = auth_client(users[2])  # outsider
    response = client.get("/projects/")
    ids = [p["id"] for p in response.json()]
    assert ids == []
