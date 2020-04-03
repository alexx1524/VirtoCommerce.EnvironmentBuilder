#! python3

import os
import sys
import argparse

from os import listdir
from os.path import join, isdir, islink, exists
from config import source_folder, modules_folder

# бранч, с которым мы работаем
branch = "feature/migrate-to-vc30"

# список модулей для обработки
vc_modules = {'Rs.AuthorizeNet':'https://github.com/Rainbow-Sandals/rs-module-authorizenet.git',
              'Rs.Core':'https://github.com/Rainbow-Sandals/rs-module-core.git',
              'Rs.Order':'https://github.com/Rainbow-Sandals/rs-module-order.git',
              'Rs.PayPal':'https://github.com/Rainbow-Sandals/rs-module-payment-paypal.git',
              'Rs.Pricing':'https://github.com/Rainbow-Sandals/rs-module-pricing.git',
              'Rs.Shipment':'https://github.com/Rainbow-Sandals/rs-module-shipment.git',
              'Rs.TaxJar':'https://github.com/Rainbow-Sandals/rs-module-taxjar.git',
              'VirtoCommerce.Cart':'https://github.com/VirtoCommerce/vc-module-cart.git',
              'VirtoCommerce.Catalog':'https://github.com/VirtoCommerce/vc-module-catalog.git',
              'VirtoCommerce.CatalogPersonalization':'https://github.com/VirtoCommerce/vc-module-catalog-personalization.git',
              'VirtoCommerce.CatalogPublishing':'https://github.com/VirtoCommerce/vc-module-catalog-publishing.git',
              'VirtoCommerce.Content':'https://github.com/VirtoCommerce/vc-module-content.git',
              'VirtoCommerce.Core':'https://github.com/VirtoCommerce/vc-module-core.git',
              'VirtoCommerce.Customer':'https://github.com/VirtoCommerce/vc-module-customer.git',
              'VirtoCommerce.CustomerReviews':'https://github.com/VirtoCommerce/vc-module-customer-review.git',
              'VirtoCommerce.ElasticSearch':'https://github.com/VirtoCommerce/vc-module-elastic-search.git',
              'VirtoCommerce.Export':'https://github.com/VirtoCommerce/vc-module-export.git',
              'VirtoCommerce.ImageTools':'https://github.com/VirtoCommerce/vc-module-image-tools.git',
              'VirtoCommerce.Inventory':'https://github.com/VirtoCommerce/vc-module-inventory.git',
              'VirtoCommerce.Marketing':'https://github.com/VirtoCommerce/vc-module-marketing.git',
              'VirtoCommerce.Notifications':'https://github.com/VirtoCommerce/vc-module-notification.git',
              'VirtoCommerce.Orders':'https://github.com/VirtoCommerce/vc-module-order.git',
              'VirtoCommerce.Payment':'https://github.com/VirtoCommerce/vc-module-payment.git',
              'VirtoCommerce.Pricing':'https://github.com/VirtoCommerce/vc-module-pricing.git',
              'VirtoCommerce.Search':'https://github.com/VirtoCommerce/vc-module-search.git',
              'VirtoCommerce.Shipping':'https://github.com/VirtoCommerce/vc-module-shipping.git',
              'VirtoCommerce.Sitemaps':'https://github.com/VirtoCommerce/vc-module-sitemaps.git',
              'VirtoCommerce.Store':'https://github.com/VirtoCommerce/vc-module-store.git',
              'VirtoCommerce.Subscription':'https://github.com/VirtoCommerce/vc-module-subscription.git',
              'VirtoCommerce.Tax':'https://github.com/VirtoCommerce/vc-module-tax.git'}

# клонирование git репозитория
def clone(path, branch, url):
    cmd = 'git clone -v --progress --branch {0} {1}'.format(branch, url)

    os.chdir(path)
    os.system(cmd)

# выполнение получения изменений в выбранной ветке
def pull(path):
    os.chdir(join(source_folder, path))
    print(join(source_folder, path))
    os.system('git pull')

# создание ссылки на web проект модуля в папке Modules платформы
def mklink(dest, src):
    print("Source: ", src)
    print("Destination: ", dest)

    if exists(dest) and islink(dest):
        print("Link {0} already exist".format(dest))
        return

    if exists(dest):
        print("{0} already exist".format(dest))
        os.rmdir(dest)
        print("{0} removed".format(dest))

    cmd = 'mklink /d "{0}" "{1}"'.format(dest, src)
    os.system(cmd)

# обработка указанного модуля
def process(module_name: str, url: str):
    print('************************************************')
    print(module_name, ": ", url)

    # get directory name fom url
    repo_folder = url[url.rfind("/")+1:][:-4]

    # create folder
    if not exists(join(source_folder, repo_folder)):
        print("Directory [{0}] created".format(module_name))

        # clone
        clone(source_folder, branch, url)

    # pull from branch
    print('Checkout [{0}]'.format(branch))
    pull(repo_folder)

    # make link
    print("Make link")

    src_path = join(sourse_folder, repo_folder, "src")

    projects = [dir for dir in listdir(src_path) if isdir(join(src_path, dir))]

    web_project_name = next(x for x in projects if x.endswith(".Web"))
    web_project_path = join(src_path, web_project_name)

    mklink(join(modules_folder, module_name), web_project_path)

    # build .net
    os.chdir(join(source_folder, repo_folder))
    os.system("dotnet build")

    # build web
    packages_file = join(web_project_path, 'package.json')
    print("Package config: ", packages_file)
    if exists(packages_file):
        os.chdir(web_project_path)
        os.system("npm install")
        os.system("npm run webpack:dev")

        # remove or discard package-lock.json
        lock_file = join(web_project_path, 'package-lock.json')
        if exists(packages_file):
            os.system('git checkout -- {0}'.format(lock_file))
    else:
        print("Package.json doesn't found")

# главный метод запуска (отрабатывает только при запуске python)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Syn tutorial')
    parser.add_argument("--mode", choices=["all-modules", "module", "theme", "storefront", "new-deploy"], required=True, type=str, help="Sync mode")
    parser.add_argument("--name", choices=list(vc_modules.keys()), required=False, type=str, help="Module name")

    args = parser.parse_args()

    mode = args.mode

    if mode == "all-modules":
        print("Sync all modules")
        for module_name, url in vc_modules.items():
            process(module_name, url)

    elif mode == "module":
        name = args.name
        print("Sync {0} module".format(name))
        if name in vc_modules:
            process(name, vc_modules[name])

    elif mode == "theme":
        pass

    elif mode == "storefront":
        pass

    elif mode == "new-deploy":
        # Полностью новый деплой в указанную папку:
        # 1. сборка и размещение платформы
        # 2. сборка и размещение сторфронта
        # 3. сборка и размещение темы
        # 4. сборка и размещение модулей и создание ссылок
        # 5. внесение настроек в appsettings.json платформы
        pass