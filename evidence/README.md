# Directory verification

[verification.json](verification.json) records the structural check of 33 capability folders, seven groups, tracked READMEs, CSV/catalog consistency and local navigation. [source-manifest.json](source-manifest.json) records source SHA-256 hashes excluding this generated evidence directory and caches.

The check runs inside a read-only OrbStack verification container. It verifies organization and links; it does not test capability implementations, vendor claims, operational controls or client work.
