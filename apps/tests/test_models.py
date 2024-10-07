import pytest
from django.db import IntegrityError
from apps.models import HomeCategory, Home, District, HomeImages, HomeNeed, Advertisement, User, Region


@pytest.mark.django_db
class TestHomeCategoryModel:
    def test_create_home_category_with_default_type(self):
        home_category = HomeCategory.objects.create()
        assert home_category.type == HomeCategory.Type.YARD
        assert home_category.type == 'Yard'

    def test_create_home_category_with_specific_type(self):
        home_category = HomeCategory.objects.create(type=HomeCategory.Type.DACHA)
        assert home_category.type == HomeCategory.Type.DACHA
        assert home_category.type == 'Dacha'

    # def test_invalid_type_choice(self):
    #     with pytest.raises(IntegrityError):
    #         HomeCategory.objects.create(type='InvalidType')

@pytest.mark.django_db
class TestHomeModel:
    @pytest.fixture
    def district(self):
        return District.objects.create(name="Central District")

    @pytest.fixture
    def home_category(self):
        return HomeCategory.objects.create(type=HomeCategory.Type.COTTAGE)

    # def test_create_home_with_defaults(self, district, home_category):
    #     home = Home.objects.create(
    #         location="123 Main St",
    #         about="A beautiful home.",
    #         home_category=home_category,
    #         district=district
    #     )
    #     assert home.type == Home.Type.ALL_PROPERTY
    #     assert home.status == Home.Status.FOR_SALE
    #     assert home.location == "123 Main St"
    #     assert home.about == "A beautiful home."
    #     assert home.home_category == home_category
    #     assert home.district == district

    # def test_create_home_with_specific_type_and_status(self, district, home_category):
    #     home = Home.objects.create(
    #         location="456 Elm St",
    #         about="A lovely rental property.",
    #         type=Home.Type.RENT,
    #         status=Home.Status.FOR_RENT,
    #         home_category=home_category,
    #         district=district
    #     )
    #     assert home.type == Home.Type.RENT
    #     assert home.status == Home.Status.FOR_RENT
    #     assert home.location == "456 Elm St"
    #     assert home.about == "A lovely rental property."
    #
    # def test_home_str_method(self, district, home_category):
    #     home = Home.objects.create(
    #         location="789 Oak St",
    #         about="Spacious business location.",
    #         type=Home.Type.BUSINESS,
    #         home_category=home_category,
    #         district=district
    #     )
    #     assert str(home) == f"{Home.Type.BUSINESS} in {home.location}"
    #
    # def test_invalid_type_choice(self, district, home_category):
    #     with pytest.raises(IntegrityError):
    #         Home.objects.create(
    #             location="000 Null St",
    #             about="Invalid type.",
    #             type="InvalidType",
    #             home_category=home_category,
    #             district=district
    #         )

    # def test_invalid_status_choice(self, district, home_category):
    #     with pytest.raises(IntegrityError):
    #         Home.objects.create(
    #             location="111 Error St",
    #             about="Invalid status.",
    #             status="InvalidStatus",
    #             home_category=home_category,
    #             district=district
    #         )

    # def test_home_requires_home_category(self, district):
    #     with pytest.raises(IntegrityError):
    #         Home.objects.create(
    #             location="222 Missing St",
    #             about="No home category.",
    #             district=district
    #         )

    def test_home_requires_district(self, home_category):
        with pytest.raises(IntegrityError):
            Home.objects.create(
                location="333 Lonely St",
                about="No district.",
                home_category=home_category
            )



