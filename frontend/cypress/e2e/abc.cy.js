describe("Todo Management Feature Tests", () => {

    let currentUserId
    let currentUserEmail
    let currentUserName

    const openTaskDetails = () => {

        cy.contains("Automation Testing Task")
            .click()
    }

    beforeEach(() => {

        cy.fixture("user.json").then((mockUser) => {

            cy.request({
                method: "POST",
                url: "http://localhost:5000/users/create",
                form: true,
                body: mockUser
            }).then((response) => {

                currentUserId = response.body._id.$oid
                currentUserEmail = mockUser.email
                currentUserName =
                    `${mockUser.firstName} ${mockUser.lastName}`

                cy.visit("http://localhost:3000")

                // login
                cy.contains("div", "Email Address")
                    .find("input[type=text]")
                    .type(currentUserEmail)

                cy.get("form").submit()

                // verify successful login
                cy.get("h1")
                    .should(
                        "contain.text",
                        `Your tasks, ${currentUserName}`
                    )

                // create a task
                cy.get(".submit-form")
                    .find("#title")
                    .type("Automation Testing Task")

                cy.get(".submit-form")
                    .find("#url")
                    .type("gWw-ytJpsqE")

                cy.get('[type="submit"]').click()

                // open task details
                openTaskDetails()
            })
        })
    })

    context("R8UC1 - Add Todo Item", () => {

        it("should create a new todo item", () => {

            cy.get('.inline-form > [type="text"]')
                .type("Practice Cypress testing")

            cy.get('.inline-form > [type="submit"]')
                .click()

            cy.get(".todo-item")
                .last()
                .should(
                    "contain.text",
                    "Practice Cypress testing"
                )
        })

        it("should disable add button for empty input", () => {

            cy.get('.inline-form > [type="submit"]')
                .should("be.disabled")
        })
    })

    context("R8UC2 - Toggle Todo Item", () => {

        it("should mark todo item as completed", () => {

            cy.contains(".todo-list", "Watch video")
                .find(".checker")
                .click()

            cy.contains("Watch video")
                .should(
                    "have.css",
                    "text-decoration-line",
                    "line-through"
                )
        })

        it("should revert completed todo item back to active", () => {

            cy.contains(".todo-list", "Watch video")
                .find(".checker")
                .click()

            cy.contains("Watch video")
                .should(
                    "have.css",
                    "text-decoration-line",
                    "line-through"
                )

            cy.contains(".todo-list", "Watch video")
                .find(".checker")
                .click()

            cy.wait(1000)

            cy.contains("Watch video")
                .should(($el) => {

                    expect(
                        $el.css("text-decoration-line")
                    ).to.not.equal("line-through")
                })
        })
    })

    context("R8UC3 - Delete Todo Item", () => {

        it("should delete selected todo item", () => {

            cy.contains(".todo-list", "Watch video")
                .find(".remover")
                .click()

            cy.contains(".todo-list", "Watch video")
                .should("not.exist")
        })
    })

    afterEach(() => {

        cy.request({
            method: "DELETE",
            url: `http://localhost:5000/users/${currentUserId}`
        }).then((response) => {

            cy.log(JSON.stringify(response.body))
        })
    })
})