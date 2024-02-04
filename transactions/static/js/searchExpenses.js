var searchExpenses = document.getElementById('searchField')
var tableOutput = document.getElementById("table-output")
var appTable = document.getElementById("app-table")
var paginationContainer = document.getElementById("pagination-container")
var tableBody = document.getElementById("table-body")
tableOutput.style.display = "none";

searchExpenses.addEventListener('keyup', function(e) {
   var searchValue = e.target.value;

   if (searchValue.trim().length > 0) {
       tableBody.innerHTML = ''
       paginationContainer.style.display = "none";

   fetch('/search_expenses', {
        body: JSON.stringify({ searchText : searchValue}),
        method: "POST",
   })
        .then((res) => res.json())
        .then((data) => {
                console.log("data", data);
                appTable.style.display = 'none';
                tableOutput.style.display = 'block';
                if (data.length === 0) {
                    tableOutput.innerHTML = 'No results found'
                }
                else {
                    data.forEach(function(item, index) {
                        tableBody.innerHTML += `
                            <tr>
                                <td>${item.amount}</td>
                                <td>${item.category}</td>
                                <td>${item.description}</td>
                                <td>${item.date}</td>
                            </tr>
                        `
                    });
                    }

             });

   }

   else {
        tableOutput.style.display = 'none';
        paginationContainer.style.display = "block";
        appTable.style.display = 'block';
   }

});
