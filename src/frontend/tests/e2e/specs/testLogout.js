describe('Checks ability to logout', () => {
  context('1080p resolution', () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      cy.viewport(1920, 1080)
      cy.visit('http://localhost:8080/')
      cy.get('#umnetId').type('umnetId')
      cy.get('#password').type('Password')
      cy.intercept('POST', '/users/login', { fixture: 'loginSuccess.json' }).as(
        'userLogin'
      )
      cy.intercept('POST', '/wallet/amount', {
        fixture: 'walletAmountEmpty.json'
      }).as('getWalletAmount')
      cy.get('#login-button').click()
      cy.wait(['@userLogin'])
      cy.wait(['@getWalletAmount'])
    })

    it('Logs user out after login', () => {
      cy.get('#nav-logout').click()

      cy.url().should('eq', 'http://localhost:8080/')
      transaction = cy.get('[class="v-toast__text"]')
      transaction.should('be.visible')
      transaction.contains('Logout successful')
    })
  })
})
