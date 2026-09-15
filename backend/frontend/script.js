const API_URL = "http://127.0.0.1:8000";


const codeInput =
    document.getElementById("codeInput");

const language =
    document.getElementById("language");

const analyzeButton =
    document.getElementById("analyzeButton");

const clearButton =
    document.getElementById("clearButton");

const lineCount =
    document.getElementById("lineCount");

const resultSection =
    document.getElementById("resultSection");

const linesResult =
    document.getElementById("linesResult");

const functionsResult =
    document.getElementById("functionsResult");

const loopsResult =
    document.getElementById("loopsResult");

const variablesResult =
    document.getElementById("variablesResult");

const syntaxResult =
    document.getElementById("syntaxResult");

const errorCard =
    document.getElementById("errorCard");

const errorList =
    document.getElementById("errorList");

const historyContainer =
    document.getElementById("historyContainer");

const refreshHistory =
    document.getElementById("refreshHistory");

const explanationContainer =
    document.getElementById("explanationContainer");

const overallExplanation =
    document.getElementById("overallExplanation");


// ---------------------------------------------
// LINE COUNTER
// ---------------------------------------------

codeInput.addEventListener(
    "input",
    function () {

        const lines =
            codeInput.value
                .split("\n")
                .filter(
                    line => line.trim() !== ""
                )
                .length;

        lineCount.textContent =
            `${lines} lines`;

    }
);


// ---------------------------------------------
// ANALYZE CODE
// ---------------------------------------------

analyzeButton.addEventListener(
    "click",
    async function () {

        const code =
            codeInput.value.trim();

        if (!code) {

            alert(
                "Please enter some code."
            );

            return;
        }


        analyzeButton.textContent =
            "Analyzing...";

        analyzeButton.disabled = true;


        try {

            const response =
                await fetch(
                    `${API_URL}/analyze`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            language:
                                language.value,

                            code: code
                        })
                    }
                );


            const data =
                await response.json();


            if (!data.success) {

                alert(data.message);

                return;
            }


            // Show result section

            resultSection
                .classList
                .remove("hidden");


            // Statistics

            linesResult.textContent =
                data.lines;

            functionsResult.textContent =
                data.functions;

            loopsResult.textContent =
                data.loops;

            variablesResult.textContent =
                data.variables;


            // Syntax

            syntaxResult.textContent =
                data.syntax_status;


            // ---------------------------------
            // CODE EXPLANATION
            // ---------------------------------

            explanationContainer.innerHTML =
                "";


            if (
                data.explanation &&
                data.explanation.length > 0
            ) {

                data.explanation.forEach(
                    function (explanation, index) {

                        const div =
                            document.createElement(
                                "div"
                            );

                        div.className =
                            "explanation-item";


                        div.innerHTML = `
                            <span class="step-number">
                                ${index + 1}
                            </span>

                            <p>
                                ${escapeHTML(
                                    explanation
                                )}
                            </p>
                        `;


                        explanationContainer
                            .appendChild(div);

                    }
                );

            }


            // Overall explanation

            overallExplanation.textContent =
                data.overall_explanation;


            // ---------------------------------
            // ERRORS
            // ---------------------------------

            if (
                data.errors &&
                data.errors.length > 0
            ) {

                errorCard
                    .classList
                    .remove("hidden");


                errorList.innerHTML =
                    "";


                data.errors.forEach(
                    function (error) {

                        const li =
                            document.createElement(
                                "li"
                            );

                        li.textContent =
                            error;

                        errorList
                            .appendChild(li);

                    }
                );

            }

            else {

                errorCard
                    .classList
                    .add("hidden");

                errorList.innerHTML =
                    "";

            }


            // Refresh history

            loadHistory();

        }


        catch (error) {

            alert(
                "Cannot connect to the backend. " +
                "Make sure FastAPI is running."
            );

            console.error(error);

        }


        finally {

            analyzeButton.textContent =
                "🔍 Analyze Code";

            analyzeButton.disabled =
                false;

        }

    }
);


// ---------------------------------------------
// CLEAR BUTTON
// ---------------------------------------------

clearButton.addEventListener(
    "click",
    function () {

        codeInput.value =
            "";

        lineCount.textContent =
            "0 lines";

        resultSection
            .classList
            .add("hidden");

    }
);


// ---------------------------------------------
// LOAD HISTORY
// ---------------------------------------------

async function loadHistory() {

    try {

        const response =
            await fetch(
                `${API_URL}/history`
            );


        const data =
            await response.json();


        historyContainer.innerHTML =
            "";


        if (
            !data.history ||
            data.history.length === 0
        ) {

            historyContainer.innerHTML =
                `
                <p class="empty-message">
                    No analysis history yet.
                </p>
                `;

            return;
        }


        data.history.forEach(
            function (item) {

                const div =
                    document.createElement(
                        "div"
                    );


                div.className =
                    "history-item";


                div.innerHTML = `

                    <div class="history-top">

                        <span
                            class="history-language"
                        >
                            ${escapeHTML(
                                item.language
                            )}
                        </span>


                        <button
                            class="delete-button"
                            onclick="deleteHistory(
                                ${item.id}
                            )"
                        >
                            Delete
                        </button>

                    </div>


                    <p>
                        Lines: ${item.lines}
                        |
                        Functions: ${item.functions}
                        |
                        Loops: ${item.loops}
                        |
                        Variables: ${item.variables}
                    </p>


                    <br>


                    <div class="history-code">

                        ${escapeHTML(
                            item.code
                        )}

                    </div>

                `;


                historyContainer
                    .appendChild(div);

            }
        );

    }


    catch (error) {

        console.error(
            "History loading error:",
            error
        );

    }

}


// ---------------------------------------------
// DELETE HISTORY
// ---------------------------------------------

async function deleteHistory(id) {

    const confirmed =
        confirm(
            "Delete this analysis?"
        );


    if (!confirmed) {

        return;
    }


    try {

        await fetch(
            `${API_URL}/history/${id}`,
            {
                method: "DELETE"
            }
        );


        loadHistory();

    }


    catch (error) {

        console.error(error);

    }

}


// ---------------------------------------------
// SECURITY FUNCTION
// ---------------------------------------------

function escapeHTML(text) {

    return text
        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


// ---------------------------------------------
// REFRESH HISTORY
// ---------------------------------------------

refreshHistory.addEventListener(
    "click",
    loadHistory
);


// Load history when page opens

loadHistory();