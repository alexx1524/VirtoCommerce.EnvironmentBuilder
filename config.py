# !!! нужно заполнить свои значения для путей
source_folder = r'C:\\Projects\\Virtoway\\RanbowSandals3\\'
platform_folder = r'C:\\Virto\\rs3.0\\VirtoCommerce.Platform\\'
modules_folder = r'C:\\Virto\\rs3.0\\VirtoCommerce.Platform\\Modules\\'

# настройки для сборки темы
theme_repository = "https://github.com/Rainbow-Sandals/rs-theme.git"
theme_branch = "feature/migrate-to-vc30"
theme_build_commands = ["npm install",
                        "gulp default"]

# настройки для сборки storefront
storefront_repository = "https://github.com/Rainbow-Sandals/rs-storefront.git"
storefront_branch = "feature/migrate-to-vc30"
storefront_build_commands = ["dotnet clear",
                             "dotnet build"]

# настройки для сборки платформы
platform_repository = "https://github.com/VirtoCommerce/vc-platform.git"
platform_branch = "feature/migrate-to-vc30"
platform_build_commands = ["dotnet clear",
                           "dotnet build"]
