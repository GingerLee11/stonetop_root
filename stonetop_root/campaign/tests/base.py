from django.test import TestCase

from campaign.models import (
    Background, Instinct, AppearanceAttribute, 
    PlaceOfOrigin, SpecialPossessions, Moves,
)

TEST_USERNAME = 'testuser'
TEST_EMAIL = 'testing@example.com'
TEST_CAMPAIGN = 'Open campaign for functional tests'


class BaseTestClass(TestCase):

    def generate_create_character_form_data(self, 
        character_class=None, background=0, 
        STR=0, DEX=0, INT=0, WIS=0, CON=0, CHA=0, 
        moves=[], **kwargs):
        background_pk = Background.objects.filter(character_class=character_class)[background].pk
        instinct_pk = Instinct.objects.filter(character_class=character_class)[0].pk
        appearance1_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance1'
        )[0].pk
        appearance2_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance2'
        )[0].pk
        appearance3_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance3'
        )[0].pk
        appearance4_pk = AppearanceAttribute.objects.filter(
            character_class=character_class).filter(
                attribute_type='appearance4'
        )[0].pk
        place_of_origin_pk = PlaceOfOrigin.objects.filter(character_class=character_class)[0].pk
        special_possession_list = SpecialPossessions.objects.filter(
            character_class__class_name=character_class
            ).order_by('possession_name')[:1]
        if moves == []:
            move_list = Moves.objects.filter(
                character_class=character_class
                ).filter(
                    move_requirements__level_restricted__isnull=True
                    ).order_by('name')[:1]
        else:
            move_list = moves
            
        form_data = {
            'background': background_pk, 
            'instinct': instinct_pk, 
            'appearance1': appearance1_pk, 
            'appearance2': appearance2_pk, 
            'appearance3': appearance3_pk, 
            'appearance4': appearance4_pk,
            'place_of_origin': place_of_origin_pk,
            'character_name': 'test',
            'strength': STR,
            'dexterity': DEX,
            'intelligence': INT,
            'wisdom': WIS,
            'constitution': CON,
            'charisma': CHA,
            'special_possessions': special_possession_list,
            'move_instances': move_list,
        }
        # Adds addtional form items for other character classes
        if kwargs:
            # print(f"\nkwargs: {kwargs}\n")
            form_kwargs = kwargs['kwargs']
            # print(f"form kwargs: {form_kwargs}\n")
            for k, v in form_kwargs.items():
                form_data[k] = v
            # print(f"form data: {form_data}\n")
        return form_data
