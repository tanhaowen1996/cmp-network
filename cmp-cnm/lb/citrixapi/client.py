from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver import csvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver_cspolicy_binding import csvserver_cspolicy_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.cspolicy import cspolicy
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csaction import csaction
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding import lbvserver_service_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.service import service
from nssrc.com.citrix.netscaler.nitro.resource.config.basic.server import server
from nssrc.com.citrix.netscaler.nitro.resource.config.network.vlan import vlan
from nssrc.com.citrix.netscaler.nitro.resource.config.network.vlan_interface_binding import vlan_interface_binding
from nssrc.com.citrix.netscaler.nitro.resource.config.ns.nsip import nsip
from cmp_cnm.settings import HTTP_FILE
import os

"""
负载均衡创建：
创建负载均衡 create_lb
4层负载均衡创建方式：
   创建4层监听：create_lb_listener -> create_lb_true_policy -> create_lb_action(action和lbvs)
   添加member：add_lb_member(lbvs_name==action_name==policy_name) -> 检查是否存在member ->(否) create_lb_member
   -> 检查是否存在server -> (否) 创建service时添加server（server_name == ipaddress）
   lb_name = lb_name
   lb_listener_name = vip:port-protocol
7层负载均衡创建方式：
   创建7层监听：create_lb_listener
   创建域名：create_lb_host(policy) -> 
   添加member：add_lb_member(lbvs_name==action_name==policy_name) -> 检查是否存在member ->(否) create_lb_member
   -> 检查是否存在server -> (否) 创建service时添加server（server_name == ipaddress）
   lb_name = lb_name
   lb_listener_name = vip:port-protocol
   lb_host_name = lb_listener_name-host_name
   lb_path_name = lb_host_name-1,lb_host_name-2....lb_host_name-n
   lb_path_name = lb_action_name = lb_vs_name
   member_name = member_ip:port-protocol
"""


def create_lb(session, name, address):
    """
    新建Content Switching vs 作为负载均衡，默认先创建一个协议为any的Content Switching
    """
    try:
        csvs = csvserver()
        csvs.name = name
        csvs.servicetype = "ANY"
        csvs.ipv46 = address
        csvs.port = "*"
        csvserver.add(session, csvs)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def delete_lb(session, name):
    try:
        csvs_list = csvserver()
        csvs_list.delete(session, name)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def get_lb(session, name):
    try:
        csvs = csvserver()
        return csvs.get(session, name)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def create_lb_listener(session, name, address, port, protocol, lbmethod):
    """
    新建4层带有端口和协议的lbvs，作为负载均衡的监听器
    """
    try:
        lb_listener = lbvserver()
        lb_listener.name = name
        lb_listener.servicetype = protocol
        lb_listener.ipv46 = address
        lb_listener.port = port
        lb_listener.lbmethod = lbmethod
        lbvserver.add(session, lb_listener)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def delete_lb_listener(session, name):
    try:
        lb_listener = lbvserver()
        lb_listener.delete(session, name)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def delete_lb_listener_csvs(session, name):
    try:
        lb_listener = csvserver()
        lb_listener.delete(session, name)
        delete_lb_ture_policy(session, name)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def delete_lb_ture_policy(session, name):
    try:
        cspolicy.delete(session, name)
        delete_lb_action(session, name)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def delete_lb_action(session, name):
    try:
        lb_action = csaction()
        lb_action.delete(session, name)
        delete_lb_vs(session, name)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def delete_lb_vs(session, name):
    try:
        lb_vserver = lbvserver()
        lb_name = name + "-lbvs"
        lb_vserver.delete(session, lb_name)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def lb_vs_member_list(session, lb_vs_name):
    """
    获取lbvs下的lb_service的列表
    """
    try:
        service_list = lbvserver_service_binding.get(session, lb_vs_name)
        if service_list:
            return service_list
        else:
            print("EXception::getservice ERROR")
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def lb_member_list(session):
    """
    获取lb下的service的列表
    """
    try:
        lb_service = service()
        result = lb_service.get(session)
        lb_member = []
        for member_name in result:
            lb_member.append(member_name.name)
        return lb_member
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def add_lb_member(session, address, port, weight, protocol, vs_name):
    """
    向vs_name的lbvs中添加lb_services
    """
    try:
        name = address + ":" + str(port) + "-" + protocol
        if name not in lb_member_list(session):
            create_lb_member(session, address, port, protocol)
        lb_member = lbvserver_service_binding()
        lb_member.servicename = name
        lb_member.weight = weight
        lb_member.name = vs_name
        lbvserver_service_binding.add(session, lb_member)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def delete_lb_member(session, name, member_name):
    try:
        lb_member = lbvserver_service_binding()
        lb_member.name = name
        lb_member.servicename = member_name
        lbvserver_service_binding.delete(session, lb_member)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def update_lb_member(session, name, member_name, ip, port, weight, protocol):
    try:
        lb_member = lbvserver_service_binding()
        lb_member.name = name
        lb_member.servicename = member_name
        lbvserver_service_binding.delete(session, lb_member)
        add_lb_member(session, ip, port, weight, protocol, name)
    except nitro_exception as exc:
        lbvserver_service_binding.add(session, lb_member)
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        lbvserver_service_binding.add(session, lb_member)
        print("Exception::message=" + str(exc.args))
        raise exc


def list_server(session):
    try:
        servers = server()
        result = servers.get(session)
        lb_servers = []
        for lb_server in result:
            lb_servers.append(lb_server.ipaddress)
        return lb_servers
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def create_lb_member(session, address, port, protocol):
    """
    新建lb_service
    """
    try:
        protocol_lb = protocol
        if protocol == "HTTPS":
            protocol_lb = "SSL"
        lb_member = service()
        lb_member.name = address + ":" + str(port) + "-" + protocol
        if address not in list_server(session):
            lb_member.ip = address
        else:
            lb_member.servername = address
        lb_member.port = port
        lb_member.servicetype = protocol_lb
        lb_member.add(session, lb_member)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def create_vlan(session, vlan_id, vlan_name):
    try:
        new_vlan = vlan()
        new_vlan.id = vlan_id
        new_vlan.aliasname = vlan_name
        vlan.add(session, new_vlan)
        vlan_bindings = vlan_interface_binding()
        vlan_bindings.id = vlan_id
        vlan_bindings.vlan_interface_bindings = "LA/1"
        vlan_bindings.tagged = True
        vlan_bindings.ifnum = "LA/1"
        vlan_interface_binding.add(session, vlan_bindings)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc


def add_snip(session, ip, netmask):
    try:
        new_ip = nsip()
        new_ip.type = "SNIP"
        new_ip.ipaddress = ip
        new_ip.netmask = netmask
        nsip.add(session, new_ip)
    except nitro_exception as exc:
        print("Exception::errorcode=" + str(exc.errorcode) + ",message=" + exc.message)
        raise exc
    except Exception as exc:
        print("Exception::message=" + str(exc.args))
        raise exc
