describe('Create Account', () => {
  context('1080p resolution', () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      cy.viewport(1920, 1080)
      cy.visit('http://localhost:8080/')
    })

    it('Successfully navigates to create account page, enters information, and logs into app', () => {
      cy.get('#create-account-link').click()
      cy.get('#umnetId').type('umnetId')
      cy.get('#password').type('Password')
      cy.get('#password2').type('Password')
      cy.get('#first-name').type('firstName')
      cy.get('#last-name').type('lastName')

      cy.intercept('POST', '/users/create', { fixture: 'success.json' }).as(
        'createAccount'
      )
      cy.intercept('POST', '/users/login', { fixture: 'loginSuccess.json' }).as(
        'userLogin'
      )
      cy.intercept('POST', '/wallet/amount', {
        fixture: 'walletAmountEmpty.json'
      }).as('getWalletAmount')

      cy.get('#create-account-button').click()
      cy.wait(['@createAccount'])
      cy.wait(['@userLogin'])
      cy.wait(['@getWalletAmount'])
      cy.url().should('eq', 'http://localhost:8080/home')
    })

    it('Displays required field empty toast', () => {
      cy.get('#create-account-link').click()
      cy.get('#password').type('Password')
      cy.get('#password2').type('Password')
      cy.get('#first-name').type('firstName')
      cy.get('#last-name').type('lastName')
      cy.get('#create-account-button').click()
      transaction = cy.get('[class="v-toast__text"]')
      transaction.should('be.visible')
      transaction.contains(
        'One or more input fields are empty. Please fill out all input fields.'
      )
    })

    it('Displays error toast when trying to create account and error occurs', () => {
      cy.get('#create-account-link').click()
      cy.get('#umnetId').type('umnetId')
      cy.get('#password').type('Password')
      cy.get('#password2').type('Password')
      cy.get('#first-name').type('firstName')
      cy.get('#last-name').type('lastName')
      cy.intercept('POST', '/users/create', {
        statusCode: 400,
        body: {
          error: 'An error occured!'
        }
      }).as('createAccount')
      cy.get('#create-account-button').click()
      cy.wait(['@createAccount'])
      transaction = cy.get('[class="v-toast__text"]')
      transaction.should('be.visible')
      transaction.contains('An error occured!')
    })
  })
})
