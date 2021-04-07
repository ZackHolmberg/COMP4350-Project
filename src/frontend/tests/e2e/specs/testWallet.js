describe('Wallet Component', () => {
  context('1080p resolution', () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      // browser with a 1080p monitor
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

    it('Validates that the wallet component is visible and looks as expected', () => {
      cy.url().should('eq', 'http://localhost:8080/home')
      wallet = cy.get('[id="wallet"]')
      wallet.should('be.visible')
      wallet.contains('0 BSC')
    })
  })
})
