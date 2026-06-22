from django.conf import settings


def upload_seed_image(instance, field_name, category, slug, src_path):
    import cloudinary.uploader

    public_id = f'media/{category}/{slug}'
    result = cloudinary.uploader.upload(
        str(src_path),
        public_id=public_id,
        overwrite=True,
        invalidate=True,
        resource_type='image',
    )

    field = getattr(instance, field_name)
    fmt = result.get('format', 'webp')
    stored_public_id = result.get('public_id', public_id)
    if stored_public_id.startswith('media/'):
        field.name = f'{stored_public_id[len("media/"):]}.{fmt}'
    else:
        field.name = f'{category}/{slug}.{fmt}'
    instance.save(update_fields=[field_name])
    return result['secure_url']


def attach_seed_image(instance, field_name, category, slug, src_path):
    if settings.USE_CLOUDINARY:
        return upload_seed_image(instance, field_name, category, slug, src_path)

    from django.core.files import File

    field = getattr(instance, field_name)
    if field and field.name:
        field.delete(save=False)

    with src_path.open('rb') as handle:
        field.save(f'{slug}.webp', File(handle), save=True)
    return field.url
