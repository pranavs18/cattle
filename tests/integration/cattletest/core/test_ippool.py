from common_fixtures import *  # NOQA


def test_subnet_ip_pool_required_fields(admin_client):
    assert_required_fields(admin_client.create_subnet_ip_pool,
                           networkAddress='192.168.3.1')


def test_subnet_ip_pool_create_delete(admin_client):
    ip_pool = admin_client.create_subnet_ip_pool(networkAddress='192.168.3.42')
    ip_pool = admin_client.wait_success(ip_pool)

    assert ip_pool.state == 'active'
    assert ip_pool.accountId is not None

    subnets = ip_pool.subnets()

    assert len(subnets) == 1

    subnet = subnets[0]

    assert subnet.state == 'active'
    assert subnet.accountId == ip_pool.accountId
    assert subnet.networkAddress == '192.168.3.42'
    assert subnet.cidrSize == 24
    assert subnet.kind == 'ipPoolSubnet'
    assert subnet.gateway == '192.168.3.1'
    assert subnet.startAddress == '192.168.3.2'
    assert subnet.endAddress == '192.168.3.250'

    ip_pool = admin_client.wait_success(ip_pool.deactivate())
    admin_client.delete(ip_pool)

    ip_pool = admin_client.wait_success(admin_client.reload(ip_pool))
    subnet = admin_client.wait_success(admin_client.reload(subnet))

    assert ip_pool.state == 'removed'
    assert subnet.state == 'removed'
    assert len(ip_pool.subnets()) == 1


def test_ip_pool_acquire(admin_client):
    ip_pool = create_and_activate(admin_client, 'ipPool')
    ip_address = ip_pool.acquire()

    assert ip_address.state == 'registering'
    assert 'associate' not in ip_address

    ip_address = admin_client.wait_success(ip_address)

    assert ip_address.kind == 'pooledIpAddress'
    assert ip_address.state == 'active'
    assert ip_address.ipPoolId == ip_pool.id


@pytest.fixture(scope='session')
def ip_pool(admin_client):
    ip_pool = create_and_activate(admin_client, 'subnetIpPool',
                                  networkAddress='192.168.3.42')
    assert len(ip_pool.subnets()) == 1
    return ip_pool


@pytest.fixture(scope='session')
def subnet(ip_pool):
    return ip_pool.subnets()[0]


def test_ip_pool_subnet_acquire(admin_client, ip_pool, subnet):
    ip_address = admin_client.wait_success(ip_pool.acquire())

    assert ip_address.kind == 'pooledIpAddress'
    assert ip_address.state == 'active'
    assert ip_address.ipPoolId == ip_pool.id
    assert ip_address.subnetId == subnet.id
    assert ip_address.address.startswith('192.168.3')
    assert 'associate' in ip_address.data.fields.capabilities


def test_ip_pool_subnet_acquire_delete_ip(admin_client, ip_pool, subnet):
    ip_address = admin_client.wait_success(ip_pool.acquire())
    ip_address = admin_client.wait_success(ip_address.deactivate())

    assert ip_address.state == 'removed'


def test_ip_address_no_associate(admin_client):
    ip = create_and_activate(admin_client, 'ipAddress')

    assert ip.state == 'active'
    assert 'associate' not in ip


def test_ip_pool_associate(admin_client, ip_pool):
    ip_address_target = admin_client.wait_success(ip_pool.acquire())
    ip_address = admin_client.wait_success(ip_pool.acquire())

    ip_address = ip_address.associate(ipAddressId=ip_address_target.id)

    assert ip_address.state == 'associating'

    ip_address = admin_client.wait_success(ip_address)

    assert ip_address.state == 'associated'

    assocs = ip_address.ipAssociations()
    assert len(assocs) == 1

    assert assocs[0].state == 'active'
    assert assocs[0].accountId == ip_address.accountId
    assert assocs[0].childIpAddressId == ip_address_target.id

    ip_address = ip_address.disassociate()

    assert ip_address.state == 'disassociating'

    ip_address = admin_client.wait_success(ip_address)

    assert ip_address.state == 'active'

    assoc = admin_client.reload(assocs[0])

    assoc = admin_client.wait_success(assoc)
    assert assoc.state == 'removed'

    assocs = ip_address.ipAssociations()
    assert len(assocs) == 1

    assert assocs[0].state == 'removed'
    assert assocs[0].removed is not None


def test_virtual_machine_with_public_ip(admin_client, sim_context, ip_pool,
                                        network):
    image_uuid = sim_context['imageUuid']
    vm = admin_client.create_virtual_machine(imageUuid=image_uuid,
                                             networkIds=[network.id],
                                             publicIpAddressPoolId=ip_pool.id)

    vm = admin_client.wait_success(vm)

    child_ip = vm.nics()[0].ipAddresses()[0]
    assocs = child_ip.childIpAssociations()

    assert len(assocs) == 1
    assert assocs[0].state == 'active'

    public_ip = assocs[0].ipAddress()

    assert public_ip.id != child_ip.id
    assert public_ip.kind == 'pooledIpAddress'
    assert 'disassociate' not in public_ip

    admin_client.delete(vm)
    vm = admin_client.wait_success(admin_client.reload(vm))

    child_ip = admin_client.wait_success(admin_client.reload(child_ip))
    public_ip = admin_client.wait_success(admin_client.reload(public_ip))
    assoc = admin_client.wait_success(admin_client.reload(assocs[0]))

    assert child_ip.state == 'active'
    assert public_ip.state == 'associated'
    assert assoc.state == 'active'

    vm = admin_client.wait_success(vm.purge())
    nic = admin_client.wait_success(vm.nics()[0])
    nic = admin_client.wait_success(nic.purge())

    child_ip = admin_client.wait_success(admin_client.reload(child_ip))
    public_ip = admin_client.wait_success(admin_client.reload(public_ip))
    assoc = admin_client.wait_success(admin_client.reload(assocs[0]))

    assert child_ip.state == 'removed'
    assert public_ip.state == 'associated'
    assert assoc.state == 'active'

    child_ip = admin_client.wait_success(child_ip.purge())
    public_ip = admin_client.wait_success(admin_client.reload(public_ip))
    assoc = admin_client.wait_success(admin_client.reload(assocs[0]))

    assert child_ip.state == 'purged'
    assert public_ip.state == 'removed'
    assert assoc.state == 'removed'


def test_virtual_machine_assigned_ip_field(admin_client, sim_context,
                                           ip_pool, network):
    image_uuid = sim_context['imageUuid']
    vm = admin_client.create_virtual_machine(imageUuid=image_uuid,
                                             networkIds=[network.id],
                                             publicIpAddressPoolId=ip_pool.id)
    vm = admin_client.wait_success(vm)

    assert vm.state == 'running'
    assert vm.primaryAssociatedIpAddress is not None

    ip = vm.nics()[0].ipAddresses()[0]
    assert vm.primaryIpAddress == ip.address

    assoc_ip = ip.childIpAssociations()[0].ipAddress()
    assert vm.primaryAssociatedIpAddress == assoc_ip.address


def test_virtual_machine_no_assigned_ip_field(admin_client, sim_context):
    image_uuid = sim_context['imageUuid']
    vm = admin_client.create_virtual_machine(imageUuid=image_uuid)
    vm = admin_client.wait_success(vm)

    assert vm.state == 'running'
    assert vm.primaryAssociatedIpAddress is None


def test_virtual_machine_with_public_ip_restart(admin_client, sim_context,
                                                ip_pool, network):
    image_uuid = sim_context['imageUuid']
    vm = admin_client.create_virtual_machine(imageUuid=image_uuid,
                                             networkIds=[network.id],
                                             publicIpAddressPoolId=ip_pool.id)

    vm = admin_client.wait_success(vm)

    assert len(vm.nics()[0].ipAddresses()[0].childIpAssociations()) == 1

    vm = admin_client.wait_success(vm.restart())

    assert len(vm.nics()[0].ipAddresses()[0].childIpAssociations()) == 1
