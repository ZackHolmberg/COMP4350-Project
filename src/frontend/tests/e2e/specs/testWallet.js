// https://docs.cypress.io/api/introduction/api.html

describe('On the homepage', () => {
  context('1080p resolution', () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      // browser with a 1080p monitor
      cy.viewport(1920, 1080)
    })

    it('Validates that the wallet component is visible and looks as expected', () => {
      wallet = cy.get('[id="wallet"]')
      wallet.should('be.visible')    
      wallet.contains("BSC")    
    })

  })
  
})


