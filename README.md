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

## Conclusion

- the issue is not to write the application, the issues are:
-- GPT is hallucinating
-- Prompts need to be extremely precise
