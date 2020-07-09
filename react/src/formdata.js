   /**
   * Retrieves input data from a form and returns it as a JSON object.
   * @param  {HTMLFormControlsCollection} elements  the form elements
   * @return {Object}                               form data as an object literal
   */
const formToJSON = elements => [].reduce.call(elements, (data, element) =>{
      
data[element.name] = element.value;
      
        return data;
      
    }, {});
    
const handleFormSubmit = event => { 
        
    event.preventDefault();
        
    const data = formToJSON_deconstructed(form.elements);
        
    };
    
const form = document.getElementsByClassName('form')[0];
form.addEventListener('submit', handleFormSubmit)

const formToJSON_deconstructed = elements => {

    const reducerFunction = (data, element) => {

        data[element.name] = element.value;

        console.log(JSON.stringify(data));
    
        return data;
  };

  const reducerInitialValue  = {};

  console.log("Initial 'data' Value:", JSON.stringify(reducerInitialValue));

  const formData = [].reduce.call(elements, reducerFunction, reducerInitialValue);

  return formData;
};