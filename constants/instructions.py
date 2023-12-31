login = "RefugEASE is an open-source humanitarian aid management system!\n\nPlease use your account details to access the application."

messages_instructions = "Below you can see your messages, separated by resolved and unresolved. You can scroll if there are many. \n\nYou can resolve / unresolve messages by selecting the message and pressing the appropriate button. \n\nNOTE: messages are sorted first by Priority (highest priority at the top), then by most recently received.\n\n- - - Sending Messages - - -\nYou can send messages by clicking the 'New message' button."

new_msg = "Please select the recipient and the urgency of the message.\n\nPlease keep your messages concise, with a maximum of 40 characters.\n\nNOTE: Plan and Camp are auto-filled according to your account."

add_edit_plan = "All fields are mandatory.\n\nStart Date must be a valid date, and cannot be before today.\n\nCentral email must be a valid email in the general format: example@domain.com."

plan_detail = "You can see information about this Plan.\n\nTotal Plan Resources is a calculated aggregation across all Camps under this Plan.\n\nCamps for this Plan can be added using the 'Add Camp' button.\n\nCamps, and their associated resources, can be viewed or edited by selecting the Camp and using the appropriate action buttons.\n\nNOTE: you can scroll to see more Camps if there are more."

new_resource = "---Input---\nCreate a new resource below.\n\nThe resource name must be unique and a max of 20 characters.\n\nUnits must be positive integers.\n\n---Submit---\n\nClick 'Submit new resource' to create the new resource."

edit_resources = "---Input---\nPlease edit existing resource amounts in the form below.\nAdd new Resource types using '+ New resource'. Only whole number amounts are allowed.\n\n ---Submit---\nClick 'Submit changes' to save any edits.\n\nNOTE: newly added resources are already saved.\n\n---Recommendations---\n\nRecommended Units Per Refugee Family Per month:\n\t- Food: 90 units\n\t- Water: 90 units\n\t- Medicine: 30 units"

camp_detail = "Information pertaining to this camp, including its Resources, Volunteers and Refugee Families can be seen here.\n\nNew Refugee Families can be registered using the '+ Add Refugee Family' button.\n\nNote: If the camp has reached full capacity, new refugee registrations will not be accepted. \n\nAccess details of registered refugee families that have departed using the 'View Departed Refugee' button.\n\nTo view or edit a particular Family, select the Family in the table and use the appropriate 'Selected Refugee Family Actions' action button."

departed_refugees = "Information about registered refugee families that have departed\n\nTo view or edit a particular Family, select the Family in the table and use the appropriate 'Selected Refugee Family Actions' action button."

add_edit_refugee = "Please fill out all the fields in the form.\n\nNOTE:\n\n- age and number of adults, children and missing people must be a valid positive integer \n\n- other fields should not exceed 40 characters max limit\n\n- please enter n/a for medical condition if not applicable"

refugee_profile = "This page displays detailed information about the corresponding refugee family. It includes personal details and current location status.\n\nTo update the information please click the 'Edit' button \n\nUse the 'Back' button to return to the Camp Details view. \n\nNote: Editing is limited to certain fields, and changes will be reflected in the overall camp management system."

INSTRUCTIONS = {
    "login": login,
    "plan_detail": plan_detail,
    "add_edit_plan": add_edit_plan,
    "camp_detail": camp_detail,
    "all_volunteers": "",
    "messages": messages_instructions,
    "new_msg": new_msg,
    "new_resource": new_resource,
    "edit_resources": edit_resources,
    "add_edit_refugee": add_edit_refugee,
    "departed_refugees": departed_refugees,
    "refugee_profile": refugee_profile,
    "search": "",
}
