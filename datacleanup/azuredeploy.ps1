function CleanString
{
    param(
        [string]$Value
    )

    return $Value.Replace("-", "")
}


function GenerateResourceName
{
    param(
        [string]$ResourceGroupName,
        [string]$Suffix
    )

    return (CleanString -Value $ResourceGroupName) + $Suffix
}

function GetResourceGroupLocation
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupName
    )

    $location = az group show `
        --name $ResourceGroupName `
        --query location `
        -o tsv

    return $location
}

function New-ArmTemplateDeployment
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$ArmTemplateUri,

        [Parameter(Mandatory = $true)]
        [hashtable]$ArmTemplateParameters,

        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupName
    )

    $armTemplateParametersJson = $ArmTemplateParameters | ConvertTo-Json

    $tempFileName = New-TemporaryFile
    Add-Content -Path $tempFileName -Value $armTemplateParametersJson

    try
    {
        az deployment group create `
        --resource-group $ResourceGroupName `
        --template-uri $ArmTemplateUri `
        --parameters """$tempFileName"""
    }
    finally
    {
        Remove-Item -Path $tempFileName -Force
    }
}

function New-DatabricksWorkspace
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupName
    )

    $generatedWorkspaceName = GenerateResourceName -ResourceGroupName $ResourceGroupName -Suffix "ws"
    $resourceGroupLocation = GetResourceGroupLocation -ResourceGroupName $ResourceGroupName

    $armTemplateParameters = @{
        pricingTier = @{ value = "premium" }
        location = @{ value = $resourceGroupLocation }
        workspaceName = @{ value = $generatedWorkspaceName }
    }

    New-ArmTemplateDeployment `
        -ArmTemplateUri "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-databricks-workspace/azuredeploy.json" `
        -ArmTemplateParameters $armTemplateParameters `
        -ResourceGroupName $ResourceGroupName

    return $generatedWorkspaceName
}

function New-StorageAccount
{
    [OutputType([hashtable])]
    param(
        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupName,

        [Parameter(Mandatory = $true)]
        [string]$ContainerName
    )

    $generatedStorageAccountName = GenerateResourceName `
        -ResourceGroupName $ResourceGroupName `
        -Suffix sto

    az storage account create `
        --name $generatedStorageAccountName `
        --resource-group $ResourceGroupName `
        --kind StorageV2 `
        --sku Standard_LRS | Out-Null

    $key = az storage account keys list `
        --account-name $generatedStorageAccountName `
        --query '[0].value' `
        -o tsv

     az storage container create `
        --name $ContainerName `
        --account-name $generatedStorageAccountName `
        --auth-mode key `
        --account-key $key | Out-Null

    return @{
        name = $generatedStorageAccountName;
        key = $key;
    }
}

function Send-BlobsToStorageContainer
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$ContainerName,

        [Parameter(Mandatory = $true)]
        [string]$SourceFolder,

        [Parameter(Mandatory = $true)]
        [string]$StorageAccountName,

        [Parameter(Mandatory = $true)]
        [string]$StorageAccountKey,

        [Parameter(Mandatory = $true)]
        [string]$FilePattern
    )

    az storage blob upload-batch `
        --destination $ContainerName `
        --source $SourceFolder `
        --account-name $StorageAccountName `
        --account-key $StorageAccountKey `
        --pattern $FilePattern
}

function New-ResourceGroup
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupName,

        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupLocation
    )

    az group create `
     --name $ResourceGroupName `
     --location $ResourceGroupLocation
}

function New-PrototypeEnvironment
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupName,

        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupLocation
    )

    Write-Warning "Starting deployment..."

    # Create resource group
    New-ResourceGroup `
        -ResourceGroupName $ResourceGroupName `
        -ResourceGroupLocation $ResourceGroupLocation

    # Create Databricks workspace
    New-DatabricksWorkspace -ResourceGroupName $ResourceGroupName

    # Create Storage account and container
    $containerName = "carsdata"

    $storageAccount = New-StorageAccount -ResourceGroupName $ResourceGroupName -ContainerName "carsdata"

    # Upload raw json data to storage container
     Send-BlobsToStorageContainer `
        -ContainerName $containerName `
        -StorageAccountName $storageAccount["name"] `
        -StorageAccountKey $storageAccount["key"] `
        -FilePattern *.json `
        -SourceFolder ".\rawdata"

    Write-Warning "Finished deployment."
}

function Remove-PrototypeEnvironment
{
    param(
        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupName
    )

    az group delete `
        --name $ResourceGroupName `
        --yes
}