from django.contrib.auth import get_user_model

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

from functional_tests.base import FunctionalTest, TEST_USERNAME, TEST_EMAIL

User = get_user_model()


class HomePageTest(FunctionalTest):

    def test_home_page_kickstarter_link_works(self):
        # Anonymous user puts in the url address for stonetop web platform site.
        self.browser.get(self.live_server_url)

        # User sees the link to the kickstarter and clicks on it
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, "Stonetop Kickstarter").click()
        )
        # They sees the kickstarter page, which has Stonetop in the Title of the page
        self.wait_for(lambda:
            self.assertIn('Stonetop', self.browser.title)
        )
    
    def test_home_page_create_campaign_link_redirects_to_login_page(self):
        # Anonymous user puts in the url address for stonetop web platform site.
        self.browser.get(self.live_server_url)

        # User sees the link to create a campaign and clicks on it
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, "Create Campaign").click()
        )
        # They sees the login page
        self.wait_for(lambda:
            self.assertIn('Login', self.browser.title)
        )
        user = self.create_user(TEST_USERNAME, TEST_EMAIL)
        self.create_pre_authenticated_session(user)
        self.browser.get(self.live_server_url)

        # User sees the link to create a campaign and clicks on it
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, "Create Campaign").click()
        )
        # They sees the page to create a campaign
        self.wait_for(lambda:
            self.assertIn('Create Campaign', self.browser.title)
        )
        

    def test_home_page_join_campaign_link_redirects_to_campaign_list(self):
        # Anonymous user puts in the url address for stonetop web platform site.
        self.browser.get(self.live_server_url)

        # User sees the link to the kickstarter and clicks on it
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, "Campaign List").click()
        )
        # They sees the Campaign List page
        self.wait_for(lambda:
            self.assertIn('Campaign List', self.browser.title)
        )


class NewUserCampaignTest(FunctionalTest):

    def test_can_create_a_campaign_and_then_view_and_update_that_campaign(self):
        # Akane has heard about a new online platform for the new Table Top RPG called Stonetop
        # She goes to checkout the homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention Stonetop
        self.assertIn('Stonetop', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Stonetop', header_text)

        # She sees the navigation bar at the top of the screen has a link saying 
        # Camapaign List 
        # She clicks on the link
        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()

        # She sees a new page; the campaign list page 
        self.wait_for(lambda:
            self.assertIn('Campaign List', self.browser.title)
        )

        # She sees that there are no available campaigns
        list_empty_list_item_text = self.browser.find_element(By.ID, 'empty-list').text
        self.assertEqual(
            'There are no available campaigns.',
            list_empty_list_item_text
        )

        # She decides that she will create a new campaign, 
        # and clicks the "Create Campaign" button below the empty campaign list.
        self.browser.find_element(By.LINK_TEXT, 'Create Campaign').click()

        # This will bring her to the login page since she has not yet logged in.
        self.wait_for(lambda: 
            self.assertIn('Login', self.browser.title)
        )
        # However, since she does not yet have an account, 
        # she will click on the "Register Here!" button.
        self.browser.find_element(By.LINK_TEXT, 'Register Here!').click()

        # This will bring her to the Registration page
        self.wait_for(lambda: 
            self.assertIn('Register', self.browser.title)
        )
        
        # Here she will fill out the relevant information to register
        ## Username: AkaneTsukino11
        ## Username: akanetsukino11@gmail.com
        self.browser.find_element(By.ID, 'id_username').send_keys('AkaneTsukino11')
        self.browser.find_element(By.ID, 'id_email').send_keys('akanetsukino11@gmail.com')
        self.browser.find_element(By.ID, 'id_password1').send_keys('SecretlyACat!')
        self.browser.find_element(By.ID, 'id_password2').send_keys('SecretlyACat!')
        self.browser.find_element(By.ID, 'id_username').send_keys(Keys.ENTER)
        
        # This will bring her back to the login page
        self.wait_for(lambda: 
            self.assertIn('Login', self.browser.title)
        )

        # She will then sign in with the credentials she just entered
        self.browser.find_element(By.ID, 'id_username').send_keys('AkaneTsukino11')
        self.browser.find_element(By.ID, 'id_password').send_keys('SecretlyACat!')
        self.browser.find_element(By.ID, 'id_username').send_keys(Keys.ENTER)

        # This should then bring her to the home page since she hasn't created an account before
        self.wait_for(lambda: 
            self.assertIn('Stonetop', self.browser.title)
        )

        # She can also see that she is now logged in
        username_text = self.browser.find_element(By.ID, 'username-nav-id').text
        self.assertIn('AkaneTsukino11', username_text)

        # She will then navigate back to the Create Campaign page
        # TODO: Make this something that can be done from the home page
        self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        self.assertIn('Campaign List', self.browser.title)
        self.browser.find_element(By.LINK_TEXT, 'Create Campaign').click()

        # She sees the create campaign page for the first time
        self.wait_for(lambda: 
            self.assertIn('Create Campaign', self.browser.title)
        )

        # She creates a new campaign
        self.browser.find_element(By.ID, 'id_name').send_keys('Cool Cats Only!')
        self.browser.find_element(By.ID, 'id_code').send_keys('KittyCatClub#11')
        self.browser.find_element(By.ID, 'id_status').send_keys(Keys.ARROW_DOWN)
        self.browser.find_element(By.ID, 'submit').click()

        # She will be taken back to the campaign list page now
        self.wait_for(lambda: 
            self.assertIn('Campaign List', self.browser.title)
        )
        
        # Where she will see her new campaign in the list
        self.assertIn(
            'Cool Cats Only!',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # She clicks on her campaign list item
        self.browser.find_element(By.ID, "id-cool-cats-only").click()

        # She sees her campaign page in all its glory!
        self.wait_for(lambda: 
            self.assertIn('Campaign Page', self.browser.title)
        )
        campaign_info = self.browser.find_element(By.ID, 'campaign-info').text
        self.assertIn('GM: AkaneTsukino11', campaign_info)
        self.assertIn('Campaign Status: Open', campaign_info)

        # Akane sees the update campaign button and clicks it
        self.browser.find_element(By.LINK_TEXT, 'Update Campaign').click()

        # She sees the update campaign page, with all the editable information
        self.wait_for(lambda: 
            self.assertIn('Update Cool Cats Only! Campaign', self.browser.title)
        )

        # She decides to change the name of the campaign to "Sakura Club"
        self.browser.find_element(By.ID, 'id_name').send_keys('Sakura Club')
        self.browser.find_element(By.ID, 'id_name').send_keys(Keys.ENTER)

        # She sees the updated name in the list of the campaigns
        self.wait_for(lambda: 
            self.assertIn(
            'Sakura Club', self.browser.find_element(By.TAG_NAME, 'body').text
        ))


class PlayersJoiningCampaignTest(FunctionalTest):

    def test_players_can_join_campaign_created_by_gm(self):
        # Samm already has a Stonetop account
        user = self.create_user('Salmontha', 'salmontha@example.com')
        self.create_pre_authenticated_session(user)

        # Log Samm out
        self.logout()
        
        # Akane is a logged in user
        user = self.create_user('AkaneTsukino11', 'AkaneTsukino11@gmail.com')
        self.create_pre_authenticated_session(user)

        # She clicks on Campaign List to create a campaign
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        )
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Create Campaign').click()
        )
        # She creates a new campaign
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_name').send_keys('Cool Cats Only!')
        )
        self.browser.find_element(By.ID, 'id_code').send_keys('KittyCatClub#11')
        self.browser.find_element(By.ID, 'id_players').send_keys('Salmontha')
        self.browser.find_element(By.ID, 'id_status').send_keys(Keys.ARROW_DOWN)
        self.browser.find_element(By.ID, 'submit').click()

        # She logs out
        self.logout()

        # Carl heard about Stonetop from Akane and wants to join the campaign
        # He visits the sites homepage
        self.browser.get(self.live_server_url)

        # Carl also has an account, Akane didn't know his username at the time
        # so sent him the campaign code afterwards
        user = self.create_user('carl@example.com', 'carl_llama')
        self.create_pre_authenticated_session(user)

        # Carl goes to the campaign List page and selects the Cool Cats Only! campaign
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        )
        self.wait_for(lambda:
            self.browser.find_element(By.ID, f'id-cool-cats-only').click()
        )
        
        # Carl then sees a message saying that he needs to enter a code into 
        # a field to see the campaign information
        self.wait_for(lambda:
            self.assertIn(
                "This is a private campaign.",
                self.browser.find_element(By.TAG_NAME, 'body').text
        ))
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Enter Code').click()
        )
        
        # TODO: See if this is the best way to check a code for the campaign

        # He accidentally enters the wrong code the first time
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').send_keys('woeifweoi3982fo2398fj')
        )
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').submit()
        )
        time.sleep(1)
        # He accidentally enters the wrong code again
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').send_keys('9238fkmdsf9283fsdfs')
        )
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').submit()
        )
        time.sleep(1)
        # He accidentally enters the wrong code again
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').send_keys('klfj2893fsldkf2938ei')
        )
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').submit()
        )
        time.sleep(1)
        # TODO: Add error messages:
        '''
        # He gets an message saying that it wasn't the correct code, 
        # and to please try again
        self.wait_for(
            msg_text = self.browser.find_element(By.CLASS_NAME, 'alert alert-warning').text
        )
        '''
        # He then enters the correct code
        self.wait_for(lambda:
            self.browser.find_element(By.ID, 'id_code').send_keys('KittyCatClub#11')
        )
        self.browser.find_element(By.ID, 'id_code').submit()

        # This will redirect Carl to the campaign detail page
        self.wait_for(lambda:
            self.assertIn('Campaign Page', self.browser.title)
        )
        campaign_info = self.browser.find_element(By.ID, 'campaign-info').text
        self.assertIn('GM: AkaneTsukino11', campaign_info)
        self.assertIn('Campaign Status: Open', campaign_info)
        self.assertNotIn('Campaign Code: KittyCatClub#11', campaign_info)
        
        # Carl will then log out.
        self.logout()

        # Samm will log back in to check the campaign status
        user = User.objects.get(username='Salmontha')
        self.create_pre_authenticated_session(user)

        # Samm goes to the campaign List page and selects the Cool Cats Only! campaign
        self.wait_for(lambda:
            self.browser.find_element(By.LINK_TEXT, 'Campaign List').click()
        )
        self.wait_for(lambda:
            self.browser.find_element(By.ID, f'id-cool-cats-only').click()
        )

        # Samm is able to see the campaign page without having to enter the campaign code, 
        # since she was added from the inception of the campaign.
        self.wait_for(lambda:
            self.assertIn('Campaign Page', self.browser.title)
        )

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        # campaign_info = self.browser.find_element(By.ID, 'campaign-info').text
        self.assertIn('GM: AkaneTsukino11', body)
        self.assertIn('Campaign Status: Open', body)
        self.assertNotIn('Campaign Code: KittyCatClub#11', body)

        # Seeing the campaign is still open, Samm logs out.
        self.logout()
         
