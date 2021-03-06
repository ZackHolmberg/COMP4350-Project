describe('On the homepage', () => {
  context('1080p resolution', () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      // browser with a 1080p monitor
      cy.viewport(1920, 1080)
      cy.visit('http://localhost:8080/')
      cy.get('#username').type('Username') 
      cy.get('#password').type('Password') 
      cy.intercept('POST', '/wallet/create', {fixture: 'success.json'}).as('createWallet')
      cy.intercept('POST', '/wallet/amount', {fixture: 'walletAmount.json'}).as('getWalletAmount')
      cy.get('#button').click()
      cy.wait(['@createWallet'])
      cy.wait(['@getWalletAmount'])
    })

    it('Validates that the wallet component is visible and looks as expected', () => {
      cy.url().should('eq', 'http://localhost:8080/home')
      wallet = cy.get('[id="wallet"]')
      wallet.should('be.visible')    
      wallet.contains("10 BSC")    
    })
  })
})


