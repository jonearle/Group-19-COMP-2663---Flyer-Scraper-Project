const openDrawer = document.getElementById('openSaves');// button that opens saved deals drawer
const closeDrawer = document.getElementById('close');//button in drawer that closes it
const sideDrawer = document.getElementById('sideDrawer');//calling the drawer itself
const addDealButtons = document.querySelectorAll('.addDealBtn');//refercne to all "Add Deal" buttons
const savedDealsList = document.getElementById('savedDealsList');//refercne to list of saved deals within drawer

// Open drawer
openDrawer.addEventListener('click', () => {
    sideDrawer.classList.add('open');
});
  
  // Close drawer
closeDrawer.addEventListener('click', () => {
    sideDrawer.classList.remove('open');
});
  
async function fetchDeals() {
    try {
        //Fetch the data from the API
        const response = await fetch('http://127.0.0.1:5000/flyerscraperapi/v1');

        //Parse the JSON data
        const deals = await response.json();

        //Render the deals
        renderDeals(deals); 
    } catch (error) {
        console.error('Error fetching deals:', error);
    }
}

function createDealCard(deal){
    
    //Create a new div for the deal card
    const newDeal = document.createElement('div');
    newDeal.className = "dealCard";

    //add name of item
    const dealTitle = document.createElement("h3");
    dealTitle.textContent = deal.Name;
    newDeal.appendChild(dealTitle);

    //add what deal is
    const dealDescription = document.createElement("p");
    dealDescription.className = "dealDescription";
    dealDescription.textContent = deal.Info;
    newDeal.appendChild(dealDescription);

    //add deal price
    const dealPrice = document.createElement("p");
    dealPrice.className = "dealPrice";
    dealPrice.textContent = deal.Price;
    newDeal.appendChild(dealPrice);


    //button to add deal to saves
    const dealButton = document.createElement('button');
    dealButton.className = "addDealBtn";
    dealButton.textContent = "Save Deal";
    newDeal.appendChild(dealButton);

    //Get the parent container where the deal card will be added
    const dealGrid = document.getElementById('dealsGrid');


    return newDeal;
}

function renderDeals(deals){

    const dealGrid = document.getElementById('dealsGrid');
    dealGrid.innerHTML = ' ';

    deals.forEach(deal => {
        const dealCard = createDealCard(deal);//create a deal cord out of each deal
        dealGrid.appendChild(dealCard);// add that deal card to the deal grid
    });
}

const dealGrid = document.getElementById('dealsGrid');
//  this allows users to save deals with all"Save Deal" buttons
dealGrid.addEventListener('click', (event) => {
    if(event.target.classList.contains('addDealBtn')){


        saveDeal(event);
    }
});

function saveDeal(event){
    const dealCard = event.target.closest('.dealCard');//this finds the parent of the button we clicked
    const savedDeal = dealCard.cloneNode(true);//we clone the deal card
    const saveDealBtn = dealCard.querySelector('.addDealBtn');

    saveDealBtn.innerHTML = "&#10003; Added";//change text to a chackmark 
    saveDealBtn.classList.add('saved');//add a saved class for styling for button
    saveDealBtn.disabled = true;//disable button so user cant add deal multiple times


    const saveButton = savedDeal.querySelector('.addDealBtn');// Remove the button from the saved deal card
    saveButton.textContent = "Remove";
    saveButton.addEventListener('click', () => removeDeal(savedDeal, dealCard));

    SavedDealsList.appendChild(savedDeal);//add our saved dealCard to our list
}

function removeDeal(savedDeal, originalDeal) {
    savedDeal.remove();

    const originalSaveButton = originalDeal.querySelector('.addDealBtn');
    originalSaveButton.textContent = "Save Deal";
    originalSaveButton.classList.remove('saved');
    originalSaveButton.disabled = false;
}

fetchDeals();

