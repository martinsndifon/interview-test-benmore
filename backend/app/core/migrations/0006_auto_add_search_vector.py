# Custom migration - Create trigger for updating the search_vector field
from django.db import migrations

# Create a custom function for updating the search_vector
update_search_vector_function = """
CREATE OR REPLACE FUNCTION update_search_vector() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('pg_catalog.english', COALESCE(NEW.title, '')), 'A');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;
"""

# Create the trigger using the custom function
search_vector_trigger = """
CREATE TRIGGER update_search_vector
BEFORE INSERT OR UPDATE ON core_project
FOR EACH ROW EXECUTE FUNCTION update_search_vector();
"""

# Drop the trigger in the reverse operation
reverse_search_vector_trigger = """
DROP TRIGGER IF EXISTS update_search_vector ON core_project;
"""


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_project_search_vector"),
    ]

    operations = [
        migrations.RunSQL(update_search_vector_function),
        migrations.RunSQL(search_vector_trigger, reverse_search_vector_trigger),
    ]
