function validateInput(input) {
    // Regular Expression to check valid input (numbers and at most one dot in the middle)
    var validPattern = /^(?![-+])\d*\.?\d*$/;
    
    // Check if the current value matches the pattern
    if (!validPattern.test(input.value)) {
        // Find the position of the last character input
        var newCursorPosition = input.selectionStart - 1;
        // Remove the last entered invalid character
        input.value = input.value.substring(0, newCursorPosition) + input.value.substring(newCursorPosition + 1);
        // Restore the cursor position
        input.setSelectionRange(newCursorPosition, newCursorPosition);
    }
}
function validateUserInput(input) {
    // Regular Expression to ensure only numeric values
    var validPattern = /^\d*$/;
    
    // Check if the current value matches the pattern
    if (!validPattern.test(input.value)) {
        // Revert to the last valid value
        input.value = input.value.slice(0, -1);
    }
}