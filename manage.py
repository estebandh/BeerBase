from flask_script import Manager
from beerbase import app, db, Style, Beer

manager = Manager(app)


# reset the database and create some initial data
@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    paleale = Style(name='Pale Ale', about='An ale made with predominantly pale malt. The highest proportion of pale malts results in a lighter color. The term "pale ale" first appeared around 1703 for beers made from malts dried with coke, which resulted in a lighter color than other beers popular at that time.')
    ipa = Style(name='American Indian Pale Ales', about='The American IPA is a different soul from the reincarnated IPA style. More flavorful than the withering English IPA, color can range from very pale golden to reddish amber. Hops are typically American with a big herbal and / or citric character, bitterness is high as well. Moderate to medium bodied with a balancing malt backbone.')
    lager = Style(name='Lager', about='Lager is a type of beer conditioned at low temperatures.[1] It may be pale, golden, amber, or dark. Pale lager is the most widely consumed and commercially available style of beer.')
    sierranevada = Beer(name='Sierra Nevada Pale Ale', hops='Cascade Hops', brewery='Sierra Nevada', style=paleale)
    yuengling = Beer(name='Yuengling IPL', hops='Cascage and Citra hops', brewery='Yuengling Brewery', style=lager)
    dogfish = Beer(name='60 Minute IPA', hops='Combination of Northwest hops', brewery='Dogfish Head Craft Brewery', style=ipa)

    db.session.add(paleale)
    db.session.add(ipa)
    db.session.add(lager)
    db.session.add(sierranevada)
    db.session.add(yuengling)
    db.session.add(dogfish)

    db.session.commit()


if __name__ == "__main__":
    manager.run()
