# anadromikAI
Recursive GPT applications

## Initial Prompt:
`echo $_GET['my_param']`

## RGPT in action:
> `<?php  echo $_GET["my_param"]; ?>`

> `<?php echo htmlspecialchars($_GET["my_param"], ENT_QUOTES); ?>`

> `echo htmlspecialchars(filter_input(INPUT_GET, 'my_param', FILTER_SANITIZE_SPECIALCHARS), ENT_QUOTES);`

> `echo htmlspecialchars(filter_input(INPUT_GET, 'my_param', FILTER_SANITIZE_STRING), ENT_QUOTES);`

> `echo htmlspecialchars(filter_input(INPUT_GET, 'my_param', FILTER_SANITIZE_STRING, ENTITY), ENTITY);`

> `echo htmlspecialchars(filter_input(INPUT_GET, 'my_param', FILTER_SANITIZE_STRING), ENTITY);`

> `echo htmlspecialchars(filter_input(INPUT_GET, 'my_param', FILTER_SANITIZE_STRING), ENTITY);`

---

## Initial Prompt
`echo the URL parameter "my_param" with php`

## RGPT in action:
`<?php echo $_GET['my_param']; ?>`

> The code you reviewed is:  `<?php echo $_GET['my_param']; ?>`
> Suggestions for improvement include: 
> 1. Sanitize the input to prevent malicious attacks such as XSS and SQL injection.  
> 2. Use a whitelist of allowed parameters instead of relying on user-supplied data in order to ensure that only valid values are accepted by your application or script. 
> 3. Consider using POST requests rather than GET, since they do not expose sensitive information in URLs which can be logged or cached publicly (eg., search engines).

```
<?php 
$my_param = filter_input(INPUT_GET, 'my_param', FILTER_SANITIZE_STRING); // sanitize input to prevent malicious attacks such as XSS and SQL injection.  
if (inarray($myParam, $allowedParams)) { // use a whitelist of allowed parameters instead of relying on user-supplied data in order to ensure that only valid values are accepted by your application or script. 	
echo $myParam; 
} ?>
```

> The code looks good overall. The use of filter_input() to sanitize user input is a great way to prevent malicious attacks such as XSS and SQL injection, which can be very dangerous for web applications. Additionally, the use of an array whitelist instead of relying on user-supplied data ensures that only valid values are accepted by your application or script. 
> However, there are some suggestions I would make in order to improve this code: 
> 1) Use strict comparison operators (===/!==) when comparing variables;  
> 2) Add error handling logic so that if any errors occur during execution they will be handled gracefully;   	
> 3) Consider using prepared statements with parameterized queries when interacting with databases in order to further protect against potential security risks like SQL injections;     
> 4) Make sure all variable names used throughout the program follow consistent naming conventions for better readability and maintainability purposes.

```
$input = filter_input(INPUT_POST, 'userInput', FILTER_SANITIZE_STRING); 
if ($input !== null && in_array($input, $whitelist)) { 
// Do something with the input 
} else { 
// Handle errors gracefully 
}
```
					
> The code looks good overall. However, there are a few suggestions I would make to improve it: 
> 1) Add additional validation checks on the user input before checking if it is in the whitelist array - this will help ensure that only valid data is being processed and reduce potential security risks. 
> 2) Use strict comparison operators (=== or !== instead of == or != ) when comparing variables for better accuracy and reliability.  
> 3) Consider using an alternative method such as filter_var() with FILTER_VALIDATE_INTEGER/FILTER_SANITIZE INTEGER depending on your needs rather than relying solely on filtering strings via filter-input(). This can provide more robust protection against malicious inputs while still allowing you to process integer values safely without having to manually validate them yourself first.

```
if (isset($_POST['userInput']) && !empty(trim($_POST['userInput']))) { 
$input = filter_var(trim($_POST['userInput']), FILTER_SANITIZE_STRING); 
    if ($input === false) { // Validate input is valid before checking whitelist array.  
        echo 'Invalid user input.';    		     	       
    } else {         
        $whitelistedValues = [1, 2, 3]; 
        if (inArray($input,$whitelistedValues)){              
            echo "Valid value";           
        } else {               
            echo "Value not in list.";            
        }
    }
} else {
    echo 'No data provided';
} 
function inArray ($valueToCheck ,$array){ 
    foreach ($array as &$val ){// Use strict comparison operator for better accuracy and reliability. 
        if ((string)$val === (string)$valueToCheck){                 
            return true ;                  
            break;
        }               
    return false ;
```
								
> Suggestions: 
> 1. Use strict comparison operator (===) for better accuracy and reliability when checking the whitelisted values array.  
> 2. Consider using a switch statement instead of an if/else block to check against multiple conditions in the same code block, as it is more efficient than nested if statements or elseif blocks with many cases that need to be checked through each iteration of looping over the whitelist array elements .   
> 3. Add additional validation checks on user input before filtering out any malicious content from being passed into your application logic by utilizing PHP's filter_var() function which can help prevent XSS attacks and other security vulnerabilities related to user data manipulation within your web applications environment .
								
```
for ($i = 0; $i < count($whitelistedValues); $i++) { 
    if (filter_var($userInput, FILTER_SANITIZE_STRING) === $whitelistedValues[$i]) {
        switch ($whitelistedValues[$i]){  	     
            case 'value1': // do something 
            break; 
            case 'value2': // do something else 
            break; 
            default: echo "Invalid input"; 
        } 
    }
```

## Conclusion

- the issue is not to write the application, the issues are:
-- GPT is hallucinating
-- Prompts need to be extremely precise
