
#Declare variables
$AZSubName = Get-AzSubscription -SubscriptionName "subname"
$AZSubID = $AZSubName.Id
$TenantID = "44467e6f-462c-4ea2-823f-7800de5434e3"
$PartnerID = "5392129"

#Select which azure subscription to use
az account set --subscription $AZSubName

#Create a new Service Principal
$sp = New-AzADServicePrincipal -DisplayName 

#Assign the Service Principal the Contributor role on the subscription
New-AzRoleAssignment `
    -ApplicationId $sp.AppId `
    -RoleDefinitionName Reader -Scope "/subscriptions/$AZSubID"

#Sign is as the service principal
$spCreds = New-AzADSpCredential -ObjectId $sp.Id
$securePassword = ConvertTo-SecureString -String $spCreds.SecretText -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential(
    $sp.AppId, 
    $securePassword
)
Connect-AzAccount `
    -ServicePrincipal `
    -Credential $credential `
    -Tenant $TenantID

#Link to the new PartnerID
New-AzManagementPartner -PartnerId $PartnerID
Get-AzManagementPartner